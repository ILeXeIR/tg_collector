from tortoise import fields, models


class Messages(models.Model):
    #The Message model
    
    id = fields.CharField(pk=True, max_length=30, generated=False)
    message_id = fields.BigIntField()
    chat_id = fields.BigIntField()
    dispatch_time = fields.CharField(max_length=30)
    sender = fields.CharField(max_length=50)
    message_type = fields.CharField(max_length=30)
    text = fields.TextField(null=True)
    attachment = fields.JSONField()

    def __str__(self):
        return self.id
