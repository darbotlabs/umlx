# Apple Foundation Models, MLX, and UMLX

Research date: 2026-10-24. This is an experimental integration consistent with
the repository's [research notice](../NOTICE.md), not a production support claim.

## Findings

The supplied screenshot shows Apple's `fm` command-line interface. Its command
list matches a first-hand macOS 27 help capture published on June 9, 2026 [1].
Apple's WWDC26 session confirms that `fm` ships with macOS 27 and demonstrates
prompting, schemas, and Python integration [2]. The capture identifies the
interface, but does not establish the availability of every command or PCC on
any particular current host. Use the installed help, not the screenshot, as the
automation contract. `probe-fm` records help and recognizes both `token-count`
and `count-tokens`; a help mention is not an inference or entitlement test.

Apple's maintained Python SDK is `apple-fm-sdk`, imported as `apple_fm_sdk`.
Its current README specifies macOS 26+, Xcode 26+, Python 3.10+, and Apple
Intelligence enabled on a compatible Mac [3]. These requirements differ from
the macOS 27 CLI requirement. The adapter uses the SDK's
`SystemLanguageModel.is_available()`, `LanguageModelSession.respond()`, and
`GenerationOptions`; it does not depend on the CLI being installed.

Foundation Models and MLX are different layers. The former provides model and
session APIs; MLX implements array computation and differentiation. MLX-LM adds
open-weight LLM loading, generation, quantization, and fine-tuning [4]. Apple's
2026 provider interface adds `LanguageModel` and `LanguageModelExecutor` and
demonstrates an `MLXFoundationModels` integration [5]. That is a useful future
Swift-facing interface for UMLX, not evidence that Apple system-model weights
can be exported, converted, or distributed through UMLX.

PCC is a separately controlled cloud capability. Apple's current access page
requires App Store Small Business Program membership, fewer than two million
first-time downloads from any of the developer's apps, and the PCC entitlement;
it describes App Store, TestFlight, and ad hoc distribution [6]. A screenshot
showing `--model pcc` does not establish a generally available cloud inference
endpoint for arbitrary servers. This integration has no PCC provider.

Upstream MLX already documents Linux CPU and CUDA packages [7]. Portability
planning should therefore separate upstream capabilities from UMLX-specific
work. Apple's provider presentation also distinguishes Core AI/ANE execution
from MLX [5]; neither an ARM CPU nor a GPU's unified memory proves NPU support.

## Repository evidence

Inspected base: `darbotlabs/umlx` commit
`14b7701723b7a538eb05194c95c6a5a2b2fa0f3a`.

| Area | Evidence at the inspected base | Implication |
| --- | --- | --- |
| Array backends | `umlx/backend/cpu`, `metal`, and `cuda`; corresponding root CMake options | Real source implementations, still requiring hardware/build validation |
| AMD ROCm and NPUs | No corresponding backend directories, CMake options, or `rocm` extra in `setup.py` | README claims exceeded implemented support |
| Python namespace | `python/umlx`; upstream MLX-LM imports `mlx.core` | Array API similarity is not drop-in package compatibility |
| Existing REST API | Array create/info/operation and device routes | No LLM loader or training API at the inspected base |
| API launcher | Uvicorn target `mlx.api.server:app` | Wrong namespace after the rebrand; corrected in this change |
| Network binding | Default `0.0.0.0:1023` | Changed to `127.0.0.1:1023` for a local inference API; host override remains explicit |

No native array backend was compiled or benchmarked during this implementation.
The README now distinguishes implemented backends from planned ones. Existing
package publication claims were not independently validated against PyPI;
the runbook below uses the checkout for UMLX.

## Applied architecture

`python/umlx/llm.py` is an optional application-layer provider adapter. It does
not import `umlx.core`, so the provider layer can be evaluated without compiling
the array extension. Existing tensor operations retain their existing runtime.

* `apple-fm`: checks the native system model, creates a fresh session per request,
  and uses the official Python SDK. Apple manages model weights and execution.
* `mlx`: sends standard chat-completion JSON to a separately running MLX-LM
  process on a literal loopback IP. The model ID is administrator configuration,
  not a caller-supplied URL. Instructions and user content retain separate roles.
* `GET /llm/providers`: reports native availability or valid MLX configuration.
  `configured` does not mean the server is reachable or weights are loaded.
* `POST /llm/respond`: shares a bounded, single-turn text contract. Unknown fields
  are rejected. Timeouts, backend errors, and refusals do not switch providers.

Loopback-only MLX transport disables inherited HTTP proxies and redirects. To
use a remote lab worker in this first version, establish an authenticated tunnel
to its loopback service. A remote authenticated provider configuration is future
work. Calling the native Apple SDK from Linux is not implemented.

The bridge intentionally keeps `mlx.*` and `umlx.*` in separate processes. Do not
inject aliases into `sys.modules`: extension types, serialization, cached tensors,
and package expectations need a compatibility suite before sharing a process.

The current adapter exposes no streaming, tools, images, structured output,
multi-turn transcripts, training, or PCC. Those limits describe this adapter,
not the full provider SDKs. Apple SDK streaming emits cumulative text snapshots,
whereas MLX APIs may emit deltas; future streaming must normalize these correctly.
The adapter reports elapsed wall time and preserves MLX's finish reason. It does
not invent Apple finish reasons, token counts, or tokens-per-second measurements.

## Run from this checkout

Python 3.10+ is required. Run from the repository root. The following installs
only Python dependencies for this provider/API experiment, not the native core:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install fastapi uvicorn pydantic httpx
export PYTHONPATH="$PWD/python"
python -m umlx.llm available
python -m umlx.llm probe-fm
```

On a compatible Mac with Apple Intelligence enabled and Xcode configured:

```bash
python -m pip install apple-fm-sdk
python -m umlx.llm respond --provider apple-fm \
  --instructions 'Extract only facts present in the text.' \
  'Summarize: the build passed 12 tests and failed 2.'
```

Review any Apple/Xcode/CLI license prompt yourself. The adapter does not accept
terms, enable Apple Intelligence, obtain an entitlement, or download system models.

Start MLX-LM in a separate terminal and environment on a supported host:

```bash
python -m venv .venv-mlx
source .venv-mlx/bin/activate
python -m pip install mlx-lm
python -m mlx_lm.server \
  --model mlx-community/Llama-3.2-3B-Instruct-4bit \
  --host 127.0.0.1 --port 8080
```

This is an upstream-documented example model, not a quality recommendation.
Check its model license and allow sufficient disk/memory for its initial download.
For Linux, consult the current MLX CPU/CUDA installation requirements [7] and
validate MLX-LM on that exact environment; an available array backend alone does
not establish every LLM architecture/kernel combination.

In the UMLX environment:

```bash
export UMLX_MLX_BASE_URL=http://127.0.0.1:8080/v1
export UMLX_MLX_MODEL=mlx-community/Llama-3.2-3B-Instruct-4bit
python -m umlx.llm respond --provider mlx 'Explain lazy array evaluation briefly.'
python -m umlx.api.server --host 127.0.0.1 --port 8100
```

Port 8100 avoids the potentially privileged legacy default 1023. Another terminal:

```bash
curl http://127.0.0.1:8100/llm/providers
curl http://127.0.0.1:8100/llm/respond \
  -H 'Content-Type: application/json' \
  -d '{"provider":"mlx","prompt":"Summarize lazy evaluation.","max_tokens":128}'
```

Change `provider` to `apple-fm` when the API process is on the compatible Mac.
For installed builds of this branch, `umlx.llm` is also a console entry point;
the `llm` extra installs HTTPX and `apple-fm` adds the Apple SDK only on macOS arm64.

## Validation and experiments

The test suite exercises routing and role preservation, SDK options and fresh
sessions, HTTP failures and timeouts, invalid completions, no automatic fallback,
loopback URL restrictions, CLI command detection, API validation, and the fixed
Uvicorn target. These are mock-provider contract tests, not native inference tests.

```bash
python -m pip install pytest
PYTHONPATH=python python -m pytest tests/test_llm_providers.py -q
python tests/validate_api.py
```

Use the same task corpus and scoring rubric for live provider comparisons:

| Experiment | Measurement | Control |
| --- | --- | --- |
| Factual extraction | exact field accuracy, unsupported claims, failure rate | fixed inputs and adjudicated expected outputs |
| Schema tasks (future adapter) | JSON validity separately from schema/semantic accuracy | identical schema subset; no prompt-only substitute for constrained decoding |
| Warm inference | p50/p95 response wall time, completion rate | explicit model/version, output budget, repeated trials |
| Cold start | first response and load time | distinguish warm server from cold weights/system assets |
| Memory/energy | process/device metrics | host-specific instrumentation; no estimate from parameter count alone |
| Cross-hardware core | operator parity, dtype tolerance, actual transfers | fixed model weights and quantization; force `mx.eval` before timing |

No live quality, speed, energy, or memory numbers are claimed. For Apple versus
an open-weight MLX model, results compare whole systems (different weights,
tokenizers, policies, and runtimes), not isolated backend efficiency.

Suggested next implementation sequence:

1. Validate native Apple and MLX-LM inference on one Mac; record OS build, SDK
   version, model identity, availability, and installed `fm --help`.
2. Implement role-preserving multi-turn and streaming adapters, including
   cumulative-snapshot handling, cancellation, and provider-specific usage.
3. Add explicit capability negotiation for tool schemas and guided generation.
4. Prototype a Swift `UMLXLanguageModel`/executor over an authenticated service,
   using the official MLX Swift provider as a reference. Model configuration
   must identify backend, weights, quantization, adapter, and session/cache scope.
5. Validate UMLX CPU/Metal/CUDA builds and `mlx.*` compatibility before claiming
   package substitution; implement ROCm and NPU paths as separate backend work.

## Sources

1. [First-hand fm help capture, June 9, 2026](https://gist.github.com/robgough/7893602895e75801174750761988ffca).
2. [Apple WWDC26: fm CLI and Python SDK](https://developer.apple.com/videos/play/wwdc2026/334/).
3. [Apple Python SDK](https://github.com/apple/python-apple-fm-sdk), inspected at
   `0249f35fce855a6701debaed569b6827fc6f5706`;
   [session implementation](https://github.com/apple/python-apple-fm-sdk/blob/0249f35fce855a6701debaed569b6827fc6f5706/src/apple_fm_sdk/session.py).
4. [MLX-LM](https://github.com/ml-explore/mlx-lm), inspected at
   `4cfc6478473b0668ede3eb0cc93f2a9181a15052`;
   [server implementation](https://github.com/ml-explore/mlx-lm/blob/4cfc6478473b0668ede3eb0cc93f2a9181a15052/mlx_lm/server.py).
5. [Apple WWDC26: LLM provider integration](https://developer.apple.com/videos/play/wwdc2026/339/)
   and [MLX Swift LM](https://github.com/ml-explore/mlx-swift-lm).
6. [Apple PCC access requirements](https://developer.apple.com/private-cloud-compute/).
7. [Upstream MLX installation and build documentation](https://ml-explore.github.io/mlx/build/html/install.html).
