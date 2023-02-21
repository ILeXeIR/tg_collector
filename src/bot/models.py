from pydantic import BaseModel


class ActiveChatPydantic(BaseModel):
    chat_id: int