from pydantic import BaseModel

class SpecializationResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class DoctorResponse(BaseModel):
    id: int
    name: str
    experience_years: int
    rating: int
    clinic_location: str
    photo_url: str | None

    class Config:
        orm_mode = True
