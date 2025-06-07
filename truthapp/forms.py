from django import forms

from truthapp.models import RecitingBoard


class RecitingBoardForm(forms.ModelForm):
    class Meta:
        model = RecitingBoard
        fields = ['audio', 'selected_meditation']
        labels = {
            'audio': '읊조림 음성',
            'selected_meditation': '묵상 파일 첨부'
        }
        widgets = {
            'audio': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'style': 'width: 90%; margin: auto; margin-bottom: 1rem;',
                'accept': 'audio/*'  # 오디오 파일만 허용
            }),
            'selected_meditation': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            })
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # 사용자의 프로필에 따라 선택지 필터링
        if self.user and hasattr(self.user, 'profile'):
            profile = self.user.profile
            choices = [('none', '첨부 안함')]

            if profile.image_medfirst:
                choices.append(('med_first', '묵상 이미지 1'))
            if profile.image_medsecond:
                choices.append(('med_second', '묵상 이미지 2'))
            if profile.video_medthird:
                choices.append(('med_video', '묵상 영상'))

            self.fields['selected_meditation'].choices = choices
        else:
            # 프로필이 없으면 첨부 안함만 선택 가능
            self.fields['selected_meditation'].choices = [('none', '첨부 안함')]