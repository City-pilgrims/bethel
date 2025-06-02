from django.utils.timezone import now
from django.contrib.auth import logout

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

            request.session['last_activity'] = now().timestamp()

        response = self.get_response(request)
        return response
