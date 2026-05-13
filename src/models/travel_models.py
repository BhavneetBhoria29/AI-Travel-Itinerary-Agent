from pydantic import BaseModel, Field
from typing import List, Optional

class Activity(BaseModel):
    """Represents a single activity in the itinerary"""
    time: str = Field(description="Time of the day for the activity (e.g., Morning, Afternoon, Evening)")
    description: str = Field(description="Detailed description of the activity")
    location: str = Field(description="Name of the place or attraction")

class DayPlan(BaseModel):
    """Represents a full day's plan"""
    day_number: int = Field(description="The day number in the trip")
    theme: str = Field(description="The main theme of the day (e.g., Historic Exploration, Beach Day)")
    activities: List[Activity] = Field(description="List of activities for the day")
    food_recommendations: List[str] = Field(description="Recommended places to eat or dishes to try")

class TravelPlan(BaseModel):
    """The final structured travel itinerary"""
    city: str = Field(description="Destination city")
    total_days: int = Field(description="Number of days planned")
    itinerary: List[DayPlan] = Field(description="The day-by-day plan")
    travel_tips: List[str] = Field(description="General travel tips and advice")
    estimated_budget_category: str = Field(description="Budget category (Budget, Mid-range, Luxury)")