from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm

CustomUser = get_user_model()  # settings.AUTH_USER_MODEL에 지정된 사용자 모델


class AccountUpdateForm(UserChangeForm):
    password = forms.CharField(
        label="새 비밀번호",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '새 비밀번호 (변경하지 않으려면 비워두세요)',
            'style': 'width: 70%; max-width: 400px; height: 40px; margin-left: auto; margin-right: auto;'
        }),
        required=False,  # 비밀번호 변경을 선택적으로 허용
    )

    password2 = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '비밀번호 확인',
            'style': 'width: 70%; max-width: 400px; height: 40px; margin-left: auto; margin-right: auto;'
        }),
        required=False,  # 비밀번호 확인은 선택적 입력
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # username 필드를 읽기 전용으로 설정
        self.fields['username'].disabled = True

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")

        if password and password2:
            if password != password2:
                raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return password2


class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': '이메일을 입력하세요',
            'style': 'width: 70%; max-width: 400px; height: 40px; margin-left: auto; margin-right: auto;'
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '비밀번호',
            'style': 'width: 70%; max-width: 400px; height: 40px; margin-left: auto; margin-right: auto;'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '비밀번호 확인',
            'style': 'width: 70%; max-width: 400px; height: 40px; margin-left: auto; margin-right: auto;'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control', 'placeholder': '아이디',
                'style': 'width: 70%; max-width: 400px; height: 40px; margin-left: auto; margin-right: auto;'
            }),
        }

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("이미 사용 중인 아이디입니다. 다른 아이디를 입력해주세요.")
        return username


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control username-field', 'placeholder': '아이디',
            'style': 'width: 70%; max-width: 400px; height: 40px; margin-left: auto; margin-right: auto;'
        })
    )
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control password-field', 'placeholder': '비밀번호',
            'style': 'width: 70%; max-width: 400px; height: 40px; margin-left: auto; margin-right: auto'
        })
    )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']