"""Shared enums and Pydantic models."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Provider(str, Enum):
    AUTO = "auto"
    GEMINI = "gemini"
    NVIDIA = "nvidia"
    OLLAMA = "ollama"


class TaskType(str, Enum):
    AUTO = "auto"
    CODE = "code"
    REVIEW = "review"
    REASONING = "reasoning"
    ARCHITECTURE = "architecture"
    VISUAL = "visual"
    CONTENT = "content"
    SPEED = "speed"


class WorkMode(str, Enum):
    ENGINEER = "engineer"
    ORCHESTRATOR = "orchestrator"


class SafetyMode(str, Enum):
    STRICT = "strict"
    BALANCED = "balanced"
    OFF = "off"


class Message(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    role: str = Field(..., description="Message role: user, assistant, or system")
    content: str = Field(..., description="Message content")


class AskInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    provider: Provider = Field(..., description="Provider to use. 'auto' enables task-aware routing.")
    prompt: str = Field(..., min_length=1, max_length=100000, description="Prompt to send.")
    model: Optional[str] = Field(default=None, description="Optional explicit model ID.")
    system_prompt: Optional[str] = Field(default=None, description="Optional system prompt.")
    temperature: Optional[float] = Field(default=None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=4096, ge=1, le=32000)
    task_type: TaskType = Field(default=TaskType.AUTO)
    timeout_seconds: Optional[float] = Field(default=None, ge=5.0, le=180.0)
    allow_fallback: bool = Field(default=True)
    include_metadata: bool = Field(default=False)
    safety_mode: SafetyMode = Field(default=SafetyMode.STRICT)
    use_cache: bool = Field(default=True)
    project_name: Optional[str] = Field(default=None, description="Project name for budgeting and observability.")
    skill_slug: Optional[str] = Field(default=None, description="Optional explicit skill to bias routing.")


class ChatInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    provider: Provider = Field(..., description="Provider to use.")
    messages: list[Message] = Field(..., min_length=1)
    model: Optional[str] = Field(default=None)
    system_prompt: Optional[str] = Field(default=None)
    temperature: Optional[float] = Field(default=None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=4096, ge=1, le=32000)
    task_type: TaskType = Field(default=TaskType.AUTO)
    timeout_seconds: Optional[float] = Field(default=None, ge=5.0, le=180.0)
    allow_fallback: bool = Field(default=True)
    include_metadata: bool = Field(default=False)
    safety_mode: SafetyMode = Field(default=SafetyMode.STRICT)
    use_cache: bool = Field(default=True)
    project_name: Optional[str] = Field(default=None)
    skill_slug: Optional[str] = Field(default=None)


class ParallelRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    id: str = Field(..., min_length=1, max_length=80)
    provider: Provider = Field(default=Provider.AUTO)
    prompt: Optional[str] = Field(default=None, min_length=1, max_length=100000)
    messages: Optional[list[Message]] = Field(default=None)
    model: Optional[str] = Field(default=None)
    system_prompt: Optional[str] = Field(default=None)
    temperature: Optional[float] = Field(default=None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=4096, ge=1, le=32000)
    task_type: TaskType = Field(default=TaskType.AUTO)
    timeout_seconds: Optional[float] = Field(default=None, ge=5.0, le=180.0)
    allow_fallback: bool = Field(default=True)
    safety_mode: SafetyMode = Field(default=SafetyMode.STRICT)
    use_cache: bool = Field(default=True)
    project_name: Optional[str] = Field(default=None)
    skill_slug: Optional[str] = Field(default=None)

    @model_validator(mode="after")
    def validate_payload(self) -> "ParallelRequest":
        if bool(self.prompt) == bool(self.messages):
            raise ValueError("Provide exactly one of 'prompt' or 'messages'")
        return self


class ParallelDispatchInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    requests: list[ParallelRequest] = Field(..., min_length=1, max_length=6)
    max_concurrency: int = Field(default=3, ge=1, le=6)
    stop_on_error: bool = Field(default=False)


class ComplexityInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    task: str = Field(..., min_length=1, max_length=20000)
    task_type: TaskType = Field(default=TaskType.AUTO)
    file_count: Optional[int] = Field(default=None, ge=0, le=1000)
    estimated_changed_lines: Optional[int] = Field(default=None, ge=0, le=20000)
    has_unknown_root_cause: bool = Field(default=False)
    needs_architecture: bool = Field(default=False)
    needs_animation: bool = Field(default=False)
    needs_visual_analysis: bool = Field(default=False)


class ModelSelectionInput(ComplexityInput):
    needs_copy: bool = Field(default=False)
    configured_only: bool = Field(default=True)
    skill_slug: Optional[str] = Field(default=None)


class OrchestrateInput(ModelSelectionInput):
    repo_context: Optional[str] = Field(default=None, max_length=40000)
    constraints: list[str] = Field(default_factory=list, max_length=20)
    preferred_mode: Optional[WorkMode] = Field(default=None)


class DiffInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    original: str = Field(..., max_length=300000)
    revised: str = Field(..., max_length=300000)
    path: str = Field(default="snippet.txt", max_length=200)
    context_lines: int = Field(default=3, ge=0, le=10)


class TextPreservationInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    original: str = Field(..., max_length=300000)
    candidate: str = Field(..., max_length=300000)
    normalize_whitespace: bool = Field(default=False)
    ignore_case: bool = Field(default=False)


class DesignAuditInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    code: str = Field(..., max_length=300000)
    profile: str = Field(default="liquid_glass", max_length=80)


class GitDiffInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    diff_text: str = Field(..., min_length=1, max_length=400000)
    context: Optional[str] = Field(default=None, max_length=10000)
    include_metadata: bool = Field(default=False)


class SkillTriggerModel(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    keywords: list[str] = Field(default_factory=list)
    file_globs: list[str] = Field(default_factory=list)
    task_types: list[str] = Field(default_factory=list)


class SkillManifestModel(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str = Field(..., min_length=1, max_length=120)
    slug: str = Field(..., min_length=1, max_length=80)
    description: str = Field(..., min_length=1, max_length=500)
    public: bool = Field(default=True)
    category: Optional[str] = Field(default=None, max_length=80)
    tags: list[str] = Field(default_factory=list)
    preferred_models: list[str] = Field(default_factory=list)
    prompt_template: str = Field(..., min_length=1)
    validation: list[str] = Field(default_factory=list)
    triggers: SkillTriggerModel = Field(default_factory=SkillTriggerModel)


for _model in [
    Message,
    AskInput,
    ChatInput,
    ParallelRequest,
    ParallelDispatchInput,
    ComplexityInput,
    ModelSelectionInput,
    OrchestrateInput,
    DiffInput,
    TextPreservationInput,
    DesignAuditInput,
    GitDiffInput,
    SkillTriggerModel,
    SkillManifestModel,
]:
    _model.model_rebuild()
