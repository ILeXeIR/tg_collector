from typing import Optional
from pydantic import BaseModel, constr


class Message_Pydantic(BaseModel):
    id: Optional[str]
    message_id: int
    chat_id: int
    dispatch_time: constr(max_length=30)
    sender: constr(max_length=50)
    message_type: constr(max_length=30)
    text: Optional[str]
    attachment: str

    class Config:
        orm_mode = True

class MessageOUT_Pydantic(Message_Pydantic):
    attachment: dict