from pydantic import BaseModel

class SymptomRequest(BaseModel):
    symptom_description: str

class TriageResponse(BaseModel):
    specialist: str
    explanation: str
