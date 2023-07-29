from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(null=True, blank=True, max_length=60)
    content = models.TextField(max_length=1500)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ('date',)

