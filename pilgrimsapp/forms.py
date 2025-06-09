from django import forms

from pilgrimsapp.models import PilgrimBoard, Question, Answer


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


class QuestionForm(forms.ModelForm):
    password = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '비밀글인 경우 비밀번호를 입력하세요'
        }),
        help_text='비밀글로 설정할 경우 비밀번호를 입력하세요.'
    )

    class Meta:
        model = Question
        fields = ['title', 'content', 'category', 'is_secret', 'password']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '제목을 입력하세요'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': '질문 내용을 상세히 작성해주세요'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_secret': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'title': '제목',
            'content': '내용',
            'category': '카테고리',
            'is_secret': '비밀글',
        }

    def clean(self):
        cleaned_data = super().clean()
        is_secret = cleaned_data.get('is_secret')
        password = cleaned_data.get('password')

        if is_secret and not password:
            raise forms.ValidationError('비밀글로 설정할 경우 비밀번호를 입력해야 합니다.')

        if not is_secret and password:
            cleaned_data['password'] = None

        return cleaned_data


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': '답변을 작성해주세요'
            }),
        }
        labels = {
            'content': '답변 내용',
        }


class SecretPasswordForm(forms.Form):
    password = forms.CharField(
        max_length=20,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '비밀번호를 입력하세요'
        }),
        label='비밀번호'
    )