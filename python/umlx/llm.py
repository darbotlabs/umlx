# Copyright © 2026 UMLX Contributors
"""Optional, explicit LLM providers above the UMLX array runtime.

Apple FM stays in Apple's SDK. MLX-LM stays in a separate process because it
imports ``mlx.*``, while this fork exposes ``umlx.*``. Neither is a tensor backend.
"""

import argparse
import asyncio
import importlib
import ipaddress
import json
import math
import os
import platform
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from urllib.parse import urlsplit


class ProviderError(RuntimeError):
    def __init__(self, message, status_code=503):
        super().__init__(message)
        self.status_code = status_code


@dataclass(frozen=True)
class GenerationRequest:
    provider: str
    prompt: str
    instructions: str = ""
    max_tokens: int = 256
    temperature: float = 0.2
    timeout: float = 60.0

    def __post_init__(self):
        if self.provider not in {"apple-fm", "mlx"}:
            raise ValueError("provider must be apple-fm or mlx")
        if not isinstance(self.prompt, str) or not self.prompt.strip():
            raise ValueError("prompt must be a nonempty string")
        if not isinstance(self.instructions, str):
            raise ValueError("instructions must be a string")
        if len(self.prompt) > 32768 or len(self.instructions) > 32768:
            raise ValueError(
                "prompt and instructions are limited to 32768 characters each"
            )
        if type(self.max_tokens) is not int or not 1 <= self.max_tokens <= 8192:
            raise ValueError("max_tokens must be an integer between 1 and 8192")
        if not math.isfinite(self.temperature) or not 0 <= self.temperature <= 2:
            raise ValueError("temperature must be finite and between 0 and 2")
        if not math.isfinite(self.timeout) or not 0 < self.timeout <= 300:
            raise ValueError("timeout must be finite and between 0 and 300 seconds")


def _apple_model():
    if platform.system() != "Darwin":
        raise ProviderError("Apple Foundation Models requires a compatible Mac")
    try:
        fm = importlib.import_module("apple_fm_sdk")
    except (ImportError, OSError) as exc:
        raise ProviderError(
            "Install apple-fm-sdk on a compatible Mac with Xcode"
        ) from exc
    try:
        model = fm.SystemLanguageModel()
        available, reason = model.is_available()
    except Exception as exc:
        raise ProviderError(
            "Apple Foundation Models availability check failed"
        ) from exc
    if not available:
        raise ProviderError(f"Apple Foundation Models unavailable: {reason}")
    return fm, model


def _mlx_config():
    model = os.environ.get("UMLX_MLX_MODEL", "").strip()
    if not model:
        raise ProviderError("Set UMLX_MLX_MODEL to the model served by MLX-LM")
    base = os.environ.get("UMLX_MLX_BASE_URL", "http://127.0.0.1:8080/v1").rstrip("/")
    try:
        url = urlsplit(base)
        host = url.hostname
        # Literal loopback addresses avoid DNS rebinding and ambiguous localhost.
        if not host or not ipaddress.ip_address(host).is_loopback:
            raise ValueError("not loopback")
        if (
            url.scheme != "http"
            or url.username
            or url.password
            or url.query
            or url.fragment
        ):
            raise ValueError("invalid URL")
        if url.path != "/v1" or (url.port is not None and url.port < 1):
            raise ValueError("expected /v1")
    except ValueError as exc:
        raise ProviderError(
            "UMLX_MLX_BASE_URL must be http://<loopback-IP>:<port>/v1"
        ) from exc
    return base, model


def provider_status():
    """Describe readiness without loading MLX weights or sending any prompts."""
    try:
        _apple_model()
        apple = {"status": "available", "detail": "System model reports available"}
    except ProviderError as exc:
        apple = {"status": "unavailable", "detail": str(exc)}
    try:
        _, model = _mlx_config()
        mlx = {
            "status": "configured",
            "model": model,
            "detail": "Endpoint configuration valid; server and weights not probed",
        }
    except ProviderError as exc:
        mlx = {"status": "unavailable", "detail": str(exc)}
    return {
        "apple-fm": apple,
        "mlx": mlx,
        "capabilities": {
            "text": True,
            "single_turn": True,
            "streaming": False,
            "tools": False,
            "structured_output": False,
            "pcc": False,
            "automatic_fallback": False,
        },
    }


async def _apple_respond(request):
    fm, model = _apple_model()
    try:
        # A fresh session prevents one caller's transcript leaking into another's.
        session = fm.LanguageModelSession(
            model=model, instructions=request.instructions or None
        )
        options = fm.GenerationOptions(
            temperature=request.temperature, maximum_response_tokens=request.max_tokens
        )
        text = await session.respond(request.prompt, options=options)
    except Exception as exc:
        # Preserve refusal/failure as failure, never retry it with another provider.
        raise ProviderError(
            "Apple Foundation Models generation failed; check model limits and policy",
            502,
        ) from exc
    if not isinstance(text, str):
        raise ProviderError("Apple Foundation Models returned a non-text response", 502)
    return text, "system", None


async def _mlx_respond(request):
    base, model = _mlx_config()
    try:
        import httpx
    except ImportError as exc:
        raise ProviderError("Install the UMLX llm extra or httpx") from exc
    messages = []
    if request.instructions:
        messages.append({"role": "system", "content": request.instructions})
    messages.append({"role": "user", "content": request.prompt})
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "max_tokens": request.max_tokens,
        "temperature": request.temperature,
    }
    try:
        # Never inherit an environment proxy or follow a redirect off this host.
        async with httpx.AsyncClient(
            timeout=request.timeout, trust_env=False, follow_redirects=False
        ) as client:
            response = await client.post(base + "/chat/completions", json=payload)
            response.raise_for_status()
            data = response.json()
    except httpx.TimeoutException as exc:
        raise ProviderError("MLX-LM request timed out", 504) from exc
    except httpx.HTTPStatusError as exc:
        raise ProviderError(
            f"MLX-LM returned HTTP {exc.response.status_code}", 502
        ) from exc
    except httpx.RequestError as exc:
        raise ProviderError("Cannot reach the local MLX-LM server") from exc
    except ValueError as exc:
        raise ProviderError("MLX-LM returned invalid JSON", 502) from exc
    try:
        choice = data["choices"][0]
        message = choice["message"]
        text = message["content"]
        if (
            message.get("tool_calls")
            or message.get("refusal")
            or not isinstance(text, str)
        ):
            raise ValueError("unsupported response")
        finish_reason = choice.get("finish_reason")
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise ProviderError(
            "MLX-LM returned no supported text completion", 502
        ) from exc
    return text, model, finish_reason


async def generate(request):
    """Execute one text request. Latency is wall time, never fabricated token speed."""
    started = time.perf_counter()
    call = _apple_respond if request.provider == "apple-fm" else _mlx_respond
    try:
        text, model, finish_reason = await asyncio.wait_for(
            call(request), request.timeout
        )
    except asyncio.TimeoutError as exc:
        raise ProviderError("Generation timed out", 504) from exc
    return {
        "provider": request.provider,
        "model": model,
        "text": text,
        "finish_reason": finish_reason,
        "elapsed_ms": (time.perf_counter() - started) * 1000,
    }


def probe_fm():
    """Capture this host's help; do not accept licenses or execute inference."""
    executable = shutil.which("fm")
    result = {
        "platform": platform.platform(),
        "executable": executable,
        "commands": [],
        "token_count_command": None,
    }
    if platform.system() != "Darwin" or executable is None:
        result["status"] = "unavailable"
        return result
    try:
        output = subprocess.run(
            [executable, "--help"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        result["status"] = "probe_failed"
        return result
    help_text = output.stdout + output.stderr
    # Require a command at the start of a help line, not a passing mention.
    commands = sorted(
        set(
            re.findall(
                r"(?m)^\s*(respond|chat|schema|serve|available|quota-usage|license|token-count|count-tokens)\s+",
                help_text,
            )
        )
    )
    result.update(
        status="help_captured" if output.returncode == 0 else "help_failed",
        exit_code=output.returncode,
        commands=commands,
        help=help_text,
    )
    result["token_count_command"] = next(
        (name for name in ("count-tokens", "token-count") if name in commands), None
    )
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser(
        "available", help="Check Apple availability and MLX configuration"
    )
    commands.add_parser("probe-fm", help="Capture the installed fm help surface")
    respond = commands.add_parser("respond", help="Generate one text response")
    respond.add_argument("prompt")
    respond.add_argument("--provider", required=True, choices=["apple-fm", "mlx"])
    respond.add_argument("--instructions", default="")
    respond.add_argument("--max-tokens", type=int, default=256)
    respond.add_argument("--temperature", type=float, default=0.2)
    respond.add_argument("--timeout", type=float, default=60)
    args = vars(parser.parse_args())
    command = args.pop("command")
    try:
        if command == "available":
            output = provider_status()
        elif command == "probe-fm":
            output = probe_fm()
        else:
            output = asyncio.run(generate(GenerationRequest(**args)))
    except (ProviderError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
