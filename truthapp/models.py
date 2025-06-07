from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class RecitingBoard(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # 업로더(작성자) 연결
    audio = models.FileField(upload_to='recite_audio/', blank=True, null=True)  # 'recite_audio/' 폴더에 저장
    created_at = models.DateTimeField(auto_now_add=True)

    MEDITATION_CHOICES = [
        ('none', '첨부 안함'),
        ('med_first', '묵상 이미지 1'),
        ('med_second', '묵상 이미지 2'),
        ('med_video', '묵상 영상'),
    ]
    selected_meditation = models.CharField(
        max_length=20,
        choices=MEDITATION_CHOICES,
        default='none',
        help_text='프로필의 묵상 파일 중 첨부할 파일을 선택하세요'
    )

    def get_attached_file(self):
        """선택된 묵상 파일 반환"""
        if not hasattr(self.author, 'profile'):
            return None

        profile = self.author.profile
        if self.selected_meditation == 'med_first' and profile.image_medfirst:
            return {'file': profile.image_medfirst, 'type': 'image'}
        elif self.selected_meditation == 'med_second' and profile.image_medsecond:
            return {'file': profile.image_medsecond, 'type': 'image'}
        elif self.selected_meditation == 'med_video' and profile.video_medthird:
            return {'file': profile.video_medthird, 'type': 'video'}
        return None

    def __str__(self):
        return f"{self.author.username} - {self.created_at.strftime('%Y-%m-%d')}"