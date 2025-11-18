from pydantic import BaseModel

class FeedbackModel(BaseModel):
    name : str
    email : str
    des : str