from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

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



class Question(models.Model):
    CATEGORY_CHOICES = [
        ('general', '일반'),
        ('tech', '창조'),
        ('account', '구원'),
        ('other', '재림'),
    ]

    title = models.CharField(max_length=200, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general', verbose_name='카테고리')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='작성자')
    is_secret = models.BooleanField(default=False, verbose_name='비밀글')
    password = models.CharField(max_length=20, blank=True, null=True, verbose_name='비밀번호')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    views = models.PositiveIntegerField(default=0, verbose_name='조회수')

    is_answered = models.BooleanField(default=False, verbose_name='답변 완료')

    class Meta:
        ordering = ['-created_at']
        verbose_name = '질문'
        verbose_name_plural = '질문들'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pilgrimsapp:detail', kwargs={'pk': self.pk})

    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers', verbose_name='질문')
    content = models.TextField(verbose_name='답변 내용')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='답변자')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    is_official = models.BooleanField(default=False, verbose_name='공식 답변')

    class Meta:
        ordering = ['created_at']
        verbose_name = '답변'
        verbose_name_plural = '답변들'

    def __str__(self):
        return f'{self.question.title}에 대한 답변'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # 답변이 등록되면 질문의 답변 완료 상태 업데이트
        if not self.question.is_answered:
            self.question.is_answered = True
            self.question.save(update_fields=['is_answered'])