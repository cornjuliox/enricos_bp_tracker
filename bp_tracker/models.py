from pydantic import BaseModel


class Event(BaseModel):
    sys: int
    dia: int
    pulse: int
    datetime: float
    notes: str
