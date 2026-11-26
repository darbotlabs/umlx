# Copyright © 2026 UMLX Contributors
"""Single-turn text API; unsupported fields are rejected, never ignored."""

from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from umlx.llm import GenerationRequest, ProviderError, generate, provider_status

router = APIRouter(prefix="/llm", tags=["Language models"])


class TextRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider: Literal["apple-fm", "mlx"]
    prompt: str = Field(min_length=1, max_length=32768)
    instructions: str = Field(default="", max_length=32768)
    max_tokens: int = Field(default=256, ge=1, le=8192, strict=True)
    temperature: float = Field(default=0.2, ge=0, le=2, allow_inf_nan=False)
    timeout: float = Field(default=60, gt=0, le=300, allow_inf_nan=False)


@router.get("/providers")
def providers():
    return provider_status()


@router.post("/respond")
async def respond(request: TextRequest):
    try:
        return await generate(GenerationRequest(**request.model_dump()))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except ProviderError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc
