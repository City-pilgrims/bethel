from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class RecitingBoard(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 업로더(작성자) 연결
    audio = models.FileField(upload_to='recite_audio/', blank=True, null=True)  # 'recite_audio/' 폴더에 저장
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.created_at.strftime('%Y-%m-%d')}"