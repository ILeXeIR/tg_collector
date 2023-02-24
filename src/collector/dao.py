from tortoise import fields, models


class Message(models.Model):
    # The Message model
    
    id = fields.UUIDField(pk=True)
    message_id = fields.BigIntField(null=True)
    chat_id = fields.BigIntField(null=True)
    dispatch_time = fields.CharField(max_length=30, null=True)
    sender = fields.CharField(max_length=50, null=True)
    message_type = fields.CharField(max_length=30)
    text = fields.TextField(null=True)
    attachment = fields.JSONField()

    def __str__(self):
        return self.id