from pydantic import BaseModel

class AnalyzeTextRequest(BaseModel):
    text: str
    highlight: str

class AnalyzeTextResponse(BaseModel):
    sentiment: str
    highlight_found: bool
    highlight_count: int
