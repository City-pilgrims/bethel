from django.contrib.auth.models import User
from django.db import models

class TimelineEvent(models.Model):
    event_date = models.DateField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="timeline_images/", null=True, blank=True)

    def __str__(self):
        return f"{self.event_date} - {self.title}"


class PilgrimBoard(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 업로더(작성자) 연결
    content = models.CharField(max_length=2000)
    image = models.FileField(upload_to='allpilgrim/')  # 'allpilgrim/' 폴더에 저장
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username} - {self.created_at.strftime('%Y-%m-%d')}"