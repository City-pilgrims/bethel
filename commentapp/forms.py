from django import forms
from django.forms import ModelForm

from commentapp.models import Comment


class CommentCreationForm(ModelForm):
    content = forms.CharField(
        widget = forms.Textarea(attrs={
                'class': 'form-control',  # form-control 클래스를 사용하여 부트스트랩 스타일 적용
                'placeholder': '댓글을 작성하세요',
                'rows': 2  # 댓글 창의 기본 크기
        }),
        required=True,
        error_messages={'required': '댓글을 입력하세요.'}
    )

    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].label = ''

        """labels = {
            'content': '댓글'  # Change the label text here
        }"""