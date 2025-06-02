from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from wayapp.models import Note


class Comment(models.Model):
    note = models.ForeignKey(Note, on_delete=models.SET_NULL, null=True, related_name='comment')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='comment')

    content = models.TextField(null=False)

    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.author.username}: {self.content[:20]}"