from django.db import models


class Message(models.Model):
    msg = models.JSONField()
