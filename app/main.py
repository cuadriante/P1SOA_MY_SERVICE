# Necessary imports
from fastapi import FastAPI
from typing import Optional

# Create the application instance
app = FastAPI()

# Define a Pydantic model for the input data (if necessary)
from pydantic import BaseModel

class RecommendationInput(BaseModel):
    type: str  # Could be 'dessert', 'main_course', 'drink'
    preferences: Optional[str] = None  # Additional preferences like 'gluten-free'

# An example endpoint that receives data to give a recommendation
@app.post("/recommend/")
async def recommend(input: RecommendationInput):
    # Here would go the logic to generate the recommendation based on the input
    return {"message": f"Recommendation for {input.type} with preferences: {input.preferences}"}

# Another example endpoint that returns a welcome message or basic information
@app.get("/")
async def root():
    return {"message": "Welcome to the recommendation service"}
