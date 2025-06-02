from django import forms

from pilgrimsapp.models import PilgrimBoard


class PilgrimBoardForm(forms.ModelForm):
    class Meta:
        model = PilgrimBoard
        fields = ['content', 'image']
        labels = {
            'content': '게시 내용 작성',  # 제목 변경
            'image': '게시 관련 이미지'
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',  # Bootstrap 스타일 적용 가능
                'style': 'width: 90%; height: 200px; resize: vertical; margin: auto; margin-bottom: 2rem;',  # 입력 창 크기 조절
                'placeholder': '게시 내용을 입력하세요'  # 힌트 텍스트 추가
            }),
        }