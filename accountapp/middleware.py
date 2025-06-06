from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib import messages
from django.utils.timezone import now


class AutoLogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            timeout_seconds = 1800  # 30분

            if last_activity and (now().timestamp() - last_activity > timeout_seconds):
                logout(request)
                request.session.flush()

                # 메시지 추가 (선택사항)
                messages.warning(request, '세션이 만료되어 로그아웃되었습니다.')

                # 로그인 페이지로 리디렉션
                return redirect('accountapp:login')

            request.session['last_activity'] = now().timestamp()

        response = self.get_response(request)
        return response

