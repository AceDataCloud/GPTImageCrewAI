"""Service-specific schemas, request fields and media shape; shared safety semantics."""

from __future__ import annotations

import json
from typing import Any, Literal

from crewai.tools.tool_failure import ToolFailure
from pydantic import BaseModel, ConfigDict, Field

from gpt_image_crewai._base import RetrieveTaskInput, ServiceTool, https_urls


class GenerateInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    model: str = Field(
        min_length=1,
        pattern=r"^gpt-image-",
        description="Current public GPT Image model ID; no alias/fallback substitution",
    )
    prompt: str = Field(min_length=1)
    size: str | None = Field(default=None, pattern=r"^(auto|\d+x\d+)$")
    quality: Literal["auto", "high", "medium", "low", "hd", "standard"] | None = None
    n: int = Field(default=1, ge=1, le=10)
    background: Literal["transparent", "opaque", "auto"] | None = None
    output_format: Literal["png", "jpeg", "webp"] | None = None
    output_compression: int | None = Field(default=None, ge=0, le=100)
    moderation: Literal["low", "auto"] | None = None


class _Tool(ServiceTool):
    service = "GPT Image"
    task_path = "/openai/tasks"

    def _media_urls(self, result: dict[str, Any]) -> list[str]:
        data = result.get("data") or []
        return https_urls(
            [item.get("url") for item in data if isinstance(item, dict)]
            if isinstance(data, list)
            else []
        )


class GPTImageGenerateImageTool(_Tool):
    name: str = "GPT Image by Ace Data Cloud - Generate Image"
    description: str = "Submit one billable GPT Image job. Save task_id, then use Retrieve Task on that same ID. Never repeat generation to poll; unknown timeouts require request-history inspection."
    args_schema: type[BaseModel] = GenerateInput
    max_usage_count: int | None = 1

    def _run(self, **parameters: Any) -> str | ToolFailure:
        payload = GenerateInput.model_validate(parameters).model_dump(exclude_none=True)
        payload["async"] = True
        payload["response_format"] = "url"
        body = self._request("/openai/images/generations", payload)
        result = self._normalize(body, "", retrieved=False)
        return result if isinstance(result, ToolFailure) else json.dumps(result)


class GPTImageRetrieveTaskTool(_Tool):
    name: str = "GPT Image by Ace Data Cloud - Retrieve Task"
    description: str = "Read an existing GPT Image task_id, optionally wait up to 240 seconds. pending is not success. This never creates new media."
    args_schema: type[BaseModel] = RetrieveTaskInput

    def _run(self, task_id: str, wait_seconds: int = 0) -> str | ToolFailure:
        return self._retrieve(task_id, wait_seconds)
