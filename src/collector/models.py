from typing import Optional
from uuid import UUID

from pydantic import BaseModel, constr


class MessageRq(BaseModel):
    message_id: Optional[int]
    chat_id: Optional[int]
    dispatch_time: Optional[constr(max_length=30)]
    sender: Optional[constr(max_length=50)]
    message_type: constr(max_length=30)
    text: Optional[str]
    attachment: str

    class Config:
        orm_mode = True

class MessageRp(MessageRq):
    id: UUID
    attachment: dict
