from pydantic import BaseModel

class Calculation(BaseModel):
    input1 : int
    input2 : int
    operator : str