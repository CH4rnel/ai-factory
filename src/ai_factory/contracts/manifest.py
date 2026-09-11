# Типизированные контракты для AI Factory (§2.2)
from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class GenerationManifest(BaseModel):
    # GenerationManifest v1 schema (§2.2)
    version: str = Field(default="1.0", description="Manifest schema version")
    job_id: str = Field(..., description="Unique job identifier")
    model: str = Field(..., description="Model name (e.g., flux1-schnell-Q4_0)")
    prompt: str = Field(..., description="User prompt")
    negative_prompt: str = Field(default="", description="Negative prompt")
    seed: int = Field(..., description="Random seed for reproducibility")
    steps: int = Field(..., ge=1, description="Number of inference steps")
    cfg_scale: float = Field(..., ge=0, description="Classifier-free guidance scale")
    width: int = Field(..., ge=64, description="Output image width")
    height: int = Field(..., ge=64, description="Output image height")
    output_path: str = Field(..., description="Path to generated output")
    # Исправлено: используем timezone-aware datetime (§50.1)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), 
        description="Creation timestamp"
    )
    metadata: Optional[dict] = Field(default=None, description="Additional metadata")


class PromptTemplate(BaseModel):
    # Prompt template с system/user ролями (§8.3)
    system: str = Field(..., description="System prompt")
    user: str = Field(..., description="User prompt template with {placeholders}")
    
    def render(self, **kwargs) -> dict:
        # Рендерит шаблон с подстановкой переменных
        return {
            "system": self.system,
            "user": self.user.format(**kwargs)
        }