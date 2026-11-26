# Copyright © 2026 UMLX Contributors
import asyncio
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import httpx
import pytest
from fastapi.testclient import TestClient
from umlx.api import server

from umlx import llm


@pytest.fixture(autouse=True)
def clean_environment(monkeypatch):
    monkeypatch.delenv("UMLX_MLX_MODEL", raising=False)
    monkeypatch.delenv("UMLX_MLX_BASE_URL", raising=False)


def use_transport(monkeypatch, handler):
    real_client = httpx.AsyncClient

    def factory(**kwargs):
        assert kwargs["trust_env"] is False
        assert kwargs["follow_redirects"] is False
        return real_client(transport=httpx.MockTransport(handler), **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", factory)
    monkeypatch.setenv("UMLX_MLX_MODEL", "example/test-model")


def test_mlx_keeps_roles_and_generation_options(monkeypatch):
    def handle(request):
        assert str(request.url) == "http://127.0.0.1:8080/v1/chat/completions"
        payload = json.loads(request.content)
        assert payload == {
            "model": "example/test-model",
            "messages": [
                {"role": "system", "content": "Be brief"},
                {"role": "user", "content": "Hello"},
            ],
            "stream": False,
            "max_tokens": 20,
            "temperature": 0.5,
        }
        return httpx.Response(
            200,
            json={"choices": [{"message": {"content": "Hi"}, "finish_reason": "stop"}]},
        )

    use_transport(monkeypatch, handle)
    result = asyncio.run(
        llm.generate(
            llm.GenerationRequest(
                "mlx", "Hello", instructions="Be brief", max_tokens=20, temperature=0.5
            )
        )
    )
    assert result["text"] == "Hi"
    assert result["finish_reason"] == "stop"
    assert result["provider"] == "mlx"
    assert result["elapsed_ms"] >= 0
    assert "tokens_per_second" not in result


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com/v1",
        "http://localhost:8080/v1",
        "http://192.168.1.2:8080/v1",
        "http://127.0.0.1:8080/v1?forward=1",
        "http://user:pass@127.0.0.1:8080/v1",
        "http://127.0.0.1:8080/other",
        "http://127.0.0.1:0/v1",
        "http://127.0.0.1:bad/v1",
    ],
)
def test_mlx_rejects_nonlocal_or_ambiguous_urls(monkeypatch, url):
    monkeypatch.setenv("UMLX_MLX_MODEL", "example/model")
    monkeypatch.setenv("UMLX_MLX_BASE_URL", url)
    with pytest.raises(llm.ProviderError, match="loopback"):
        llm._mlx_config()


def test_ipv6_loopback(monkeypatch):
    monkeypatch.setenv("UMLX_MLX_MODEL", "example/model")
    monkeypatch.setenv("UMLX_MLX_BASE_URL", "http://[::1]:8080/v1/")
    assert llm._mlx_config() == ("http://[::1]:8080/v1", "example/model")


@pytest.mark.parametrize(
    "body",
    [
        {},
        {"choices": []},
        {"choices": [{"message": {"content": None}}]},
        {"choices": [{"message": {"content": "", "tool_calls": [{"id": "x"}]}}]},
        {"choices": [{"message": {"content": "", "refusal": "declined"}}]},
    ],
)
def test_malformed_or_unsupported_completion_fails(monkeypatch, body):
    use_transport(monkeypatch, lambda request: httpx.Response(200, json=body))
    with pytest.raises(llm.ProviderError) as error:
        asyncio.run(llm.generate(llm.GenerationRequest("mlx", "hello")))
    assert error.value.status_code == 502


@pytest.mark.parametrize("status", [302, 400, 429, 500])
def test_http_failure_is_not_fallback(monkeypatch, status):
    use_transport(
        monkeypatch,
        lambda request: httpx.Response(
            status, headers={"Location": "https://example.com/v1"}
        ),
    )
    apple = AsyncMock()
    monkeypatch.setattr(llm, "_apple_respond", apple)
    with pytest.raises(llm.ProviderError, match=f"HTTP {status}"):
        asyncio.run(llm.generate(llm.GenerationRequest("mlx", "hello")))
    apple.assert_not_called()


def test_http_timeout(monkeypatch):
    def handle(request):
        raise httpx.ReadTimeout("test", request=request)

    use_transport(monkeypatch, handle)
    with pytest.raises(llm.ProviderError) as error:
        asyncio.run(llm.generate(llm.GenerationRequest("mlx", "hello")))
    assert error.value.status_code == 504


def test_native_sdk_uses_fresh_session_and_options(monkeypatch):
    sessions = []
    model = SimpleNamespace(is_available=lambda: (True, None))

    def make_session(**kwargs):
        assert kwargs == {"model": model, "instructions": "Be concise"}
        session = SimpleNamespace(respond=AsyncMock(return_value="native answer"))
        sessions.append(session)
        return session

    sdk = SimpleNamespace(
        SystemLanguageModel=lambda: model,
        LanguageModelSession=make_session,
        GenerationOptions=lambda **kwargs: kwargs,
    )
    monkeypatch.setattr(llm.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(llm.importlib, "import_module", lambda name: sdk)
    request = llm.GenerationRequest("apple-fm", "hello", instructions="Be concise")
    for _ in range(2):
        result = asyncio.run(llm.generate(request))
        assert result["model"] == "system"
        assert result["text"] == "native answer"
    assert len(sessions) == 2
    sessions[0].respond.assert_awaited_once_with(
        "hello", options={"temperature": 0.2, "maximum_response_tokens": 256}
    )


def test_apple_refusal_does_not_fall_back(monkeypatch):
    sdk = SimpleNamespace(
        LanguageModelSession=lambda **kw: SimpleNamespace(
            respond=AsyncMock(side_effect=RuntimeError("refusal"))
        ),
        GenerationOptions=lambda **kw: kw,
    )
    monkeypatch.setattr(llm, "_apple_model", lambda: (sdk, object()))
    fallback = AsyncMock()
    monkeypatch.setattr(llm, "_mlx_respond", fallback)
    with pytest.raises(llm.ProviderError, match="generation failed"):
        asyncio.run(llm.generate(llm.GenerationRequest("apple-fm", "hello")))
    fallback.assert_not_called()


def test_non_mac_does_not_import_sdk(monkeypatch):
    monkeypatch.setattr(llm.platform, "system", lambda: "Linux")
    importer = Mock(side_effect=AssertionError("SDK must not load"))
    monkeypatch.setattr(llm.importlib, "import_module", importer)
    status = llm.provider_status()
    assert status["apple-fm"]["status"] == "unavailable"
    assert status["mlx"]["status"] == "unavailable"
    importer.assert_not_called()


def test_configured_does_not_claim_model_loaded(monkeypatch):
    monkeypatch.setattr(llm.platform, "system", lambda: "Linux")
    monkeypatch.setenv("UMLX_MLX_MODEL", "example/model")
    assert llm.provider_status()["mlx"]["status"] == "configured"


@pytest.mark.parametrize("command", ["token-count", "count-tokens"])
def test_fm_probe_detects_both_surfaces(monkeypatch, command):
    monkeypatch.setattr(llm.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(llm.shutil, "which", lambda name: "/usr/bin/fm")
    runner = Mock(
        return_value=SimpleNamespace(
            returncode=0,
            stderr="",
            stdout=(
                f"COMMANDS\n  respond Generate\n  {command} Count tokens\n  serve Serve\n"
            ),
        )
    )
    monkeypatch.setattr(llm.subprocess, "run", runner)
    result = llm.probe_fm()
    assert result["token_count_command"] == command
    assert result["commands"] == sorted(["respond", command, "serve"])
    assert runner.call_args.args == (["/usr/bin/fm", "--help"],)


@pytest.mark.parametrize(
    "changes",
    [
        {"provider": "pcc"},
        {"prompt": " "},
        {"max_tokens": 0},
        {"max_tokens": True},
        {"temperature": float("nan")},
        {"timeout": 301},
    ],
)
def test_invalid_request(changes):
    values = {"provider": "mlx", "prompt": "hello"}
    values.update(changes)
    with pytest.raises(ValueError):
        llm.GenerationRequest(**values)


@pytest.mark.parametrize(
    "extra", [{"stream": True}, {"tools": []}, {"url": "http://x"}]
)
def test_api_rejects_unsupported_options(extra):
    with TestClient(server.app) as client:
        response = client.post(
            "/llm/respond", json={"provider": "mlx", "prompt": "hello", **extra}
        )
    assert response.status_code == 422


def test_api_success_and_unavailable(monkeypatch):
    use_transport(
        monkeypatch,
        lambda request: httpx.Response(
            200,
            json={
                "choices": [
                    {"message": {"content": "hello"}, "finish_reason": "length"}
                ]
            },
        ),
    )
    with TestClient(server.app) as client:
        response = client.post("/llm/respond", json={"provider": "mlx", "prompt": "hi"})
        assert response.status_code == 200
        assert response.json()["finish_reason"] == "length"
        monkeypatch.delenv("UMLX_MLX_MODEL")
        assert (
            client.post(
                "/llm/respond", json={"provider": "mlx", "prompt": "hi"}
            ).status_code
            == 503
        )


def test_api_start_target_and_loopback_default(monkeypatch):
    runner = Mock()
    monkeypatch.setattr(server.uvicorn, "run", runner)
    server.start_server()
    assert runner.call_args.args == ("umlx.api.server:app",)
    assert runner.call_args.kwargs["host"] == "127.0.0.1"
