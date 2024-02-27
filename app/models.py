from pydantic import BaseModel

class RecommendationRequest(BaseModel):
    description: str
    src: str