from typing import List, Optional

from pydantic import BaseModel, Field


class CodeRequest(BaseModel):
    code: str = Field(..., description="Source code to analyze")
    language: str = Field("auto", description="Language name or auto")


class Issue(BaseModel):
    line: Optional[int] = Field(
        default=None,
        description="Line number where the issue was detected"
    )
    severity: str = Field(..., description="Issue severity such as low, medium, or high")
    category: str = Field(..., description="Issue category such as syntax, style, or security")
    message: str = Field(..., description="Short issue message")
    suggestion: str = Field(..., description="Recommended fix")


class CodeResponse(BaseModel):
    summary: str = Field(..., description="Short analysis summary")
    language: str = Field(..., description="Detected or selected language")
    issues: List[Issue] = Field(default_factory=list, description="List of detected issues")
    fixed_code: Optional[str] = Field(
        default=None,
        description="AI-generated or rule-based fixed code"
    )