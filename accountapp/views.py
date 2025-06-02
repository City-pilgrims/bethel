from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your views here.
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from accountapp.decorators import account_ownership_required
from accountapp.forms import AccountUpdateForm, CustomLoginForm, CustomUser, CustomSignupForm

has_ownership = [account_ownership_required, login_required]


class AccountCreateView(CreateView):
    model = CustomUser
    form_class = CustomSignupForm
    template_name = 'accountapp/create.html'
    success_url = reverse_lazy('pilgrimsapp:intro')  # 회원가입 후 이동할 페이지

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # 회원가입 후 자동 로그인
        return redirect(self.success_url)


class AccountDetailView(DetailView):
    model = User
    context_object_name = 'target_user'
    template_name = 'accountapp/detail.html'


@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountUpdateView(UpdateView):
    model = CustomUser
    context_object_name = 'target_user'
    form_class = AccountUpdateForm
    success_url = reverse_lazy('truthapp:index')
    template_name = 'accountapp/update.html'

    def form_valid(self, form):
        user = form.save(commit=False)

        # 비밀번호 변경 처리
        password = form.cleaned_data.get("password")
        if password:  # 새 비밀번호가 입력된 경우
            user.set_password(password)
            update_session_auth_hash(self.request, user)  # 로그아웃 방지

        user.save()
        return super().form_valid(form)


@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountDeleteView(DeleteView):
    model = User
    context_object_name = 'target_user'
    success_url = reverse_lazy('accountapp:login')
    template_name = 'accountapp/delete.html'


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'accountapp/login.html'

    def get_redirect_url(self):
        # 'next' 파라미터를 GET 데이터에서 가져옵니다
        next_url = self.request.GET.get('next','/')
        redirect_to = self.request.GET.get('next')

        # 만약 'next'가 회원가입 페이지를 가리킨다면, 다른 페이지로 리디렉션
        if '/accounts/create/' in next_url:
            # 기본 페이지로 리디렉션 (예: 홈 페이지)
            return reverse('pilgrimsapp:intro')  # 적절한 URL로 변경하세요

        elif '/accounts/login/' in next_url:
            # 기본 페이지로 리디렉션 (예: 홈 페이지)
            return reverse('pilgrimsapp:intro')

        elif not redirect_to:  # 예제: 존재하지 않는 페이지일 경우
            return reverse('pilgrimsapp:intro')

        return next_url