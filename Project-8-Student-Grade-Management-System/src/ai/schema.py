from pydantic import BaseModel


class AISummaryResponse(BaseModel):
    summary: str

