from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile') #onetoonefield user와 profile을 연결해주는것

    image = models.ImageField(upload_to='profile/', null=True)
    nickname = models.CharField(max_length=20, unique=True, null=True)
    message = models.CharField(max_length=200, null=True)

    # 묵상에서 활용하기 위해서 추가됨
    image_medfirst = models.ImageField(upload_to='profile_img_med/', null=True, blank=True)
    image_medsecond = models.ImageField(upload_to='profile_img_med/', null=True, blank=True)
    video_medthird = models.FileField(upload_to='profile_video_med/', null=True, blank=True)