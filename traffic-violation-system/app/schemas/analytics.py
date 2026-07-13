from pydantic import BaseModel, Field

class AnalyticsSummaryResponse(BaseModel):
    total_violations: int = Field(..., description="Cumulative count of all violations logged")
    total_vehicles: int = Field(0, description="Total distinct vehicles tracked")
    helmet_cases: int = Field(..., description="Total cases of helmet violations")
    seatbelt_cases: int = Field(..., description="Total cases of seatbelt violations")
    red_light_cases: int = Field(..., description="Total cases of red light violations")

    model_config = {
        "from_attributes": True
    }

class DailyStatItem(BaseModel):
    date: str = Field(..., description="Formatted date label")
    count: int = Field(..., description="Violation count for this day")

class TypeStatItem(BaseModel):
    type: str = Field(..., description="Violation classification label")
    count: int = Field(..., description="Infraction count")
