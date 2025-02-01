from io import BytesIO

from PIL import Image
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.base import ContentFile
from django.db import models

# Create your models here.
from django.urls import reverse
from django_lifecycle import LifecycleModelMixin
from taggit.managers import TaggableManager
from typing import List


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Note(LifecycleModelMixin, TimeStampedModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    tags = TaggableManager(blank=True, help_text="쉼표로 구분하여 작성해주세요.")

    class Meta:
        ordering = ["-pk"]

    def get_absolute_url(self) -> str:
        return reverse("wayapp:detail", kwargs={"pk": self.pk})


class Photo(TimeStampedModel):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='pilgrim/')

    @classmethod
    def create_photos(cls, note: Note, photo_file_list: List[File]) -> List["Photo"]:
        if not note.pk:
            raise ValueError("Note를 먼저 저장해주세요.")

        photo_list = []
        for photo_file in photo_file_list:
            photo = cls(note=note)

            img = Image.open(photo_file)
            img_format = img.format
            #img.show()
            #exif_data = img.getexif()

            min_size = min(img.size)
            left = (img.width - min_size) / 2
            top = (img.height - min_size) / 2
            right = (img.width + min_size) / 2
            bottom = (img.height + min_size) / 2
            img = img.crop((left, top, right, bottom))

            # 이미지 리사이즈 (예: 300x300 픽셀)
            if min_size > 700:
                resized_img = img.resize((700, 700), Image.ANTIALIAS)
            else:
                resized_img = img.resize((min_size, min_size), Image.ANTIALIAS)

            buffer = BytesIO()
            resized_img.save(buffer,format=img_format)
            buffer.seek(0)
            photo_file_rev = ContentFile(buffer.getvalue(), name=f'processed_{photo_file.name}')

            photo.image.save(photo_file.name, photo_file_rev, save=False)
            photo_list.append(photo)

        cls.objects.bulk_create(photo_list)

        return photo_list








