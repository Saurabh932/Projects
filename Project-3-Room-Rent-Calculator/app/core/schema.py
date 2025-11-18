from pydantic import BaseModel

class RentModel(BaseModel):
    room_rent : int
    food : int
    wifi : int
    electricity : int
    no_person : int
    