from django import forms
from django.forms import ModelForm

from profileapp.models import Profile


class ProfileCreationForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'nickname', 'message', 'image_medfirst', 'image_medsecond', 'video_medthird']
        labels = {
            'image': '프로필 이미지',
            'nickname': '닉네임',
            'message': '메시지',
            'image_medfirst': '묵상 이미지1',
            'image_medsecond': '묵상 이미지2',
            'video_medthird': '묵상 영상'
        }
        widgets = {
            'image': forms.FileInput(attrs={
                'style': 'display: block; margin: 0 auto; width: 70%;',  # 이미지 업로드 입력창의 폭을 90%로 설정
            }),
            'nickname': forms.TextInput(attrs={
                'style': 'width: 80%; height: 40px; margin: 0 auto',  # 입력 창 크기 조절
            }),
            'message': forms.Textarea(attrs={
                'rows': 5,
                'cols': 40,
                'class': 'form-control center-input',  # Bootstrap 스타일 적용 가능
                'style': 'width: 80%; height: 80px; resize: none; word-wrap: break-word; margin: 0 auto',  # 입력 창 크기 조절
                'placeholder': '제목을 입력하세요'  # 힌트 텍스트 추가
            }),
            'image_medfirst': forms.FileInput(attrs={
                'style': 'display: block; margin: 0 auto; width: 70%;',  # 이미지 업로드 입력창의 폭을 90%로 설정
            }),
            'image_medsecond': forms.FileInput(attrs={
                'style': 'display: block; margin: 0 auto; width: 70%;',  # 이미지 업로드 입력창의 폭을 90%로 설정
            }),
            'video_medthird': forms.FileInput(attrs={
                'style': 'display: block; margin: 0 auto; width: 70%;',  # 이미지 업로드 입력창의 폭을 90%로 설정
            }),
        }

