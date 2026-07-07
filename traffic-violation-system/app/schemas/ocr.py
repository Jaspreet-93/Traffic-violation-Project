from pydantic import BaseModel, Field

class OCRStatusResponse(BaseModel):
    running: bool = Field(..., description="Flag indicating if real-time plate OCR is enabled")

class OCRStartResponse(BaseModel):
    message: str = Field(..., description="API success confirmation message")
    status: str = Field(..., description="Status flag indicating current state")

class OCRStopResponse(BaseModel):
    message: str = Field(..., description="API success confirmation message")
    status: str = Field(..., description="Status flag indicating current state")

class OCRResultResponse(BaseModel):
    vehicle_id: int = Field(..., description="Associated vehicle tracking ID")
    plate_number: str = Field(..., description="Extracted vehicle registration character string")
    confidence: float = Field(..., description="Character recognition confidence score")
