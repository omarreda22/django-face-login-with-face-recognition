from django.db import models
from twilio.rest import Client


class Score(models.Model):
    result = models.PositiveIntegerField()

    def __str__(self):
        return str(self.result)

    def save(self, *args, **kwargs):
        account_sid = "AC78d77aa0307511a57e81513421ed63c8"
        auth_token = "201592414112c60006d56eb3d980d497"
        client = Client(account_sid, auth_token)
        message = client.messages \
                        .create(
                            body="Hello there.",
                            from_='+13159225952',
                            to='+201554648636'
                        )
        return super().save(*args, **kwargs)