from pydantic import BaseModel

class Points(BaseModel):
    points: list[tuple[float, float]]