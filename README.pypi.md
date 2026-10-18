# GPT Image by Ace Data Cloud for CrewAI

Independent native **GPT Image** image tools for CrewAI. Provided by **Ace Data Cloud**, not an official GPT Image or CrewAI product. This is a standalone service package; no all-services bundle or generic provider setup is required.

[简体中文](https://github.com/AceDataCloud/GPTImageCrewAI/blob/0eea3c3c57067d82680ba54680db29ddce08eb51/readme/README_zh_Hans.md) · [Current models and prices](https://platform.acedata.cloud/models?utm_source=pypi&utm_medium=referral&utm_campaign=evergreen&utm_content=gptimagecrewai_package_pricing)

## 1. Install the stable release

The Ace-maintained **GPTImage** native CrewAI tools are merged on main and released as **0.1.0**. This is a standalone service package. It is **not an official CrewAI/AMP catalog listing**, and no PyPI publication is claimed yet. Install the public wheel with its exact SHA256:

```bash
uv add 'crewai-gpt-image @ https://github.com/AceDataCloud/GPTImageCrewAI/releases/download/v0.1.0/crewai_gpt_image-0.1.0-py3-none-any.whl#sha256=6051bd70f833e1c05dc9bae405a23ee6316818efc50deeb38e95a4926b37068e'
```

Or install the exact merged source:

```bash
uv add 'crewai-gpt-image @ git+https://github.com/AceDataCloud/GPTImageCrewAI.git@0eea3c3c57067d82680ba54680db29ddce08eb51'
```

[Stable release](https://github.com/AceDataCloud/GPTImageCrewAI/releases/tag/v0.1.0) · [Merged source](https://github.com/AceDataCloud/GPTImageCrewAI/commit/0eea3c3c57067d82680ba54680db29ddce08eb51). Tags and pages are informational; the immutable source SHA or wheel SHA256 binds the artifact. Historical previews remain unchanged and are not the recommended version. When an existing authorized PyPI publisher can publish after the shared new-project quota resets, the normal `uv add crewai-gpt-image` command will become available; do not assume publication before registry readback.

CrewAI requires Python3.10–3.13. Complete Linux installation, tests and clean-wheel checks passed. Intel macOS may lack the mandatory lancedb wheel; use a supported Linux environment instead of skipping dependencies for production.

## 2. Register / sign in and get your own API Token

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=pypi&utm_medium=referral&utm_campaign=evergreen&utm_content=gptimagecrewai_package_api_key); register and sign in. If needed, choose **Initialize General Application**.
2. Open **General application**, check **GPT Image** service access, current model price and balance. A service-specific application can only use its entitled service.
3. Copy the selected API Key using icon **1**, or **Manage Keys** **2** → **Create** for a separate `GPT Image CrewAI` key.

![Copy Key or open Manage Keys; authentic screenshot with credentials redacted](https://raw.githubusercontent.com/AceDataCloud/GPTImageCrewAI/0eea3c3c57067d82680ba54680db29ddce08eb51/assets/tutorial/get-api-key-en.png)

4. Configure expiration and usage limits only as needed. If **Allowed APIs** is enabled, include both `/openai/images/generations` and `/openai/tasks`.

![Create a separate credential; historical example name](https://raw.githubusercontent.com/AceDataCloud/GPTImageCrewAI/0eea3c3c57067d82680ba54680db29ddce08eb51/assets/tutorial/create-api-key-en.png)

Historical authentic Ace screenshots reused unchanged from SunoDify commit `8d3d03570e73324220f111f7fe343da0792a8071`, retrieved 2026-10-18. The second image's old name `Dify tutorial` is an example only: use `GPT Image CrewAI`. No visible real credential is included; [image sources](https://raw.githubusercontent.com/AceDataCloud/GPTImageCrewAI/0eea3c3c57067d82680ba54680db29ddce08eb51/assets/tutorial/source.json).

Set the raw consumer Token in environment variable `ACEDATACLOUD_API_KEY` through secure terminal input or a secret manager. It is not a `platform-...` management Token and must not include `Bearer `, spaces or quotation marks. Never place it in prompts, screenshots, committed `.env` or workflow exports. `api_key=...` may be supplied from secure credential storage and is excluded from serialization.

## 3. Add the named native tools

```python
from crewai import Agent
from gpt_image_crewai import GPTImageGenerateImageTool, GPTImageRetrieveTaskTool

agent = Agent(
    role="GPT Image producer",
    goal="Create the approved media, then retrieve the original task result",
    backstory="Use GPT Image through Ace Data Cloud within the user's approved budget.",
    llm=your_configured_llm,
    tools=[GPTImageGenerateImageTool(), GPTImageRetrieveTaskTool()],
    allow_delegation=False,
    max_retry_limit=0,
)
```

The two discoverable tool names are **GPT Image by Ace Data Cloud - Generate Image** and **GPT Image by Ace Data Cloud - Retrieve Task**. The Token goes in the environment, not a custom MCP header or agent prompt. Adding tools does not execute them. The caller approves paid requests; generation defaults to one use per instance to reduce duplicate submissions, which is not a funds cap or a permission system.

## 4. Service-specific input and first use

GPT Image generation only: current `gpt-image-*` model, prompt, size (`auto` or WIDTHxHEIGHT), quality, n 1..10, background, output_format/compression and moderation. Uses `/openai/images/generations`, `response_format=url`, and asynchronous same-task queries. This is not the built-in DallETool, Nano Banana or a general image-provider alias. Image editing/multipart is not included in this first package.

Check [the current model catalog and price](https://platform.acedata.cloud/models?utm_source=pypi&utm_medium=referral&utm_campaign=evergreen&utm_content=gptimagecrewai_package_first_use) before calling; model IDs are passed unchanged and no substitute model is added. The following values are examples from the pinned current API contract, not permanent defaults. **Executing generation is billable**; this guide does not run it.

```python
import json
from gpt_image_crewai import GPTImageGenerateImageTool, GPTImageRetrieveTaskTool

parameters = {
    "model": "gpt-image-2",
    "prompt": "A red apple on a plain white background",
    "size": "1024x1024",
    "quality": "low",
    "n": 1
}
# BILLABLE when executed; approve the current model and budget first.
submitted = GPTImageGenerateImageTool().run(**parameters)
submitted = json.loads(submitted)  # A ToolFailure must be handled before this step.
task_id = submitted["task_id"]
result = GPTImageRetrieveTaskTool().run(task_id=task_id, wait_seconds=240)
print(result)
```

The request submits once with `async=true`. accepted/pending is **not** a terminal result, even when an envelope has success=true. Preserve the original task ID; pending, timeouts or unknown submission outcomes do not authorize another generation. Bounded wait only queries that same ID, and can include an in-flight request timeout. Continue using Retrieve Task until terminal status. A true completed response requires the stored finished_at, service success and a valid target media URL. Nested failed states are treated as failure; a missing terminal media link is not fake success.

For a task you already own, run only this read-only example:

```bash
uv run python examples/query_existing.py YOUR_EXISTING_TASK_ID
```

The query is `POST /openai/tasks` with `action=retrieve,id=...`. A completed result returns `status=succeeded`, `success=true`, `task_id`, filtered `media_urls` and original `cost` in Credits when present. No raw original prompt, request, account/application identity, internal diagnostics or unfiltered body is returned. `cost` is not a new bill or USD amount. URL presence does not verify ongoing media playback.

## 5. Inspect execution and output

![Official historical CrewAI execution trace; not this service or Ace runtime evidence](https://raw.githubusercontent.com/AceDataCloud/GPTImageCrewAI/0eea3c3c57067d82680ba54680db29ddce08eb51/assets/tutorial/official-crewai-tracing.png)

Official [CrewAI tracing reference](https://docs.crewai.com/en/observability/tracing), historical date marker 10/1/2025, capture version unspecified; retrieved 2026-10-18. Left: task and tool timeline; right: expanded Response output, not input. **Not this package running, not an Ace task and not a promised new GUI.** Trace account/auth/consent is optional and not enabled by this package. For your actual run inspect the named tool and its returned terminal fields; never expose Token or private media URLs in screenshots.

## Troubleshooting, privacy and cost

| Result | Action |
|---|---|
| 401 / 403 | Check full raw consumer Token, expiration, service entitlement, Allowed APIs and balance. A 403 is not always moderation. |
| 400 / schema rejection | Follow this service's fields, casing and model capability; unknown cross-service fields are rejected before network. |
| pending / no media yet | Query the same original task ID; never regenerate to poll. |
| 429 | Reduce concurrency and wait. One HTTP attempt per operation; your configured LLM/agent may retry separately. |
| Timeout / 5xx | Submission outcome can be unknown. Inspect request history before creating another task. |
| ToolFailure | Failed task or invalid terminal media; structured non-retryable result. Preserve task/trace ID for support, never Key. |
| Result URL cannot open | Check terminal success and your network; link existence alone is not playback evidence. |

The code is free; media generation and the LLM you configure have their current prices. No payment handler, fallback or automatic paid HTTP retry is added. Original Credits cost follows the API's current package/account rate and discounts; this package does not hard-code USD conversion. No install/CI count is presented as users or revenue.

Provided prompts/references and the consumer Token are sent to `api.acedata.cloud` over HTTPS. The package adds no telemetry or tracing; CrewAI/your LLM may have separate settings. [Privacy](https://github.com/AceDataCloud/GPTImageCrewAI/blob/0eea3c3c57067d82680ba54680db29ddce08eb51/PRIVACY.md). [Source](https://github.com/AceDataCloud/GPTImageCrewAI) · [Issues](https://github.com/AceDataCloud/GPTImageCrewAI/issues) · dev@acedata.cloud

Development: `uv sync --group dev`, `uv run pytest`, `uv run ruff check .`, `uv build`. Paid HTTP is mocked in tests; native Agent/Task/Crew cycles use a deterministic local model fixture. See `tests/contract-source.json` for immutable service contract provenance and `tests/live-readonly-evidence.json` when an old-task check is available. No new paid request runs in CI.
