from tortoise import fields, models


class ActiveChats(models.Model):
    # A list of active chats

    chat_id = fields.BigIntField(pk=True, generated=False)

    def __str__(self):
        return self.chat_id