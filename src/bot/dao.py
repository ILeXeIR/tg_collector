from aiogram import Bot
from aiogram.fsm.storage.base import BaseStorage, StateType, StorageKey
from tortoise import fields, models
from typing import Optional


class ActiveChat(models.Model):
    # A list of active chats

    chat_id = fields.BigIntField(pk=True, generated=False)

    def __str__(self):
        return self.chat_id


class CustomStorageMeta(type(models.Model), type(BaseStorage)):
    pass


class CustomStorage(models.Model, BaseStorage, metaclass=CustomStorageMeta):
    # A table for states of FSM

    id = fields.UUIDField(pk=True)
    chat_id = fields.BigIntField()
    user_id = fields.BigIntField()
    state = fields.CharField(max_length=30)

    async def get_state(self, bot: Bot, key: StorageKey) -> Optional[str]:
        state_obj = await self.get_or_none(chat_id=key.chat_id,
                                           user_id=key.user_id)
        return state_obj.state if state_obj is not None else None

    async def set_state(
            self, bot: Bot, key: StorageKey, state: StateType) -> None:
        await self.filter(chat_id=key.chat_id, user_id=key.user_id).delete()
        if state is not None:
            await self.create(
                chat_id=key.chat_id,
                user_id=key.user_id,
                state=state.state
            )

    async def set_data(self, bot: Bot, key: StorageKey, data: dict):
        pass

    async def get_data(self, bot: Bot, key: StorageKey):
        pass

    async def close(self):
        pass
