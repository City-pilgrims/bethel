from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
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


class AccountDetailView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'target_user'
    template_name = 'accountapp/detail.html'
    login_url = '/accounts/login/'

    # 로그인 후 다시 이 페이지로 오도록 설정
    redirect_field_name = 'next'


@method_decorator(has_ownership, 'dispatch')
class AccountUpdateView(UpdateView):
    model = CustomUser
    context_object_name = 'target_user'
    form_class = AccountUpdateForm
    template_name = 'accountapp/update.html'

    def get_success_url(self):
        return reverse_lazy('accountapp:detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        user = form.save(commit=False)

        # 새 비밀번호 처리 (필드명 변경됨)
        new_password = form.cleaned_data.get("new_password")
        if new_password:  # 새 비밀번호가 입력된 경우
            user.set_password(new_password)
            update_session_auth_hash(self.request, user)  # 로그아웃 방지

        user.save()
        return super().form_valid(form)


@method_decorator(has_ownership, 'dispatch')
class AccountDeleteView(DeleteView):
    model = User
    context_object_name = 'target_user'
    success_url = reverse_lazy('accountapp:login')
    template_name = 'accountapp/delete.html'


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'accountapp/login.html'

    def get_redirect_url(self):
        next_url = self.request.GET.get('next', '/')

        # 차단할 URL 목록
        blocked_urls = ['/accounts/create/', '/accounts/login/']

        # 차단된 URL인 경우 intro로 리디렉션
        if any(blocked_url in next_url for blocked_url in blocked_urls):
            return reverse('pilgrimsapp:intro')

        # 루트 URL(/)인 경우에만 intro로 리디렉션
        if next_url == '/':
            return reverse('pilgrimsapp:intro')

        # 나머지 모든 경우는 원래 URL로 리디렉션 (MyPage 포함)
        return next_url