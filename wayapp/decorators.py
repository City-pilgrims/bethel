from django.contrib.auth.models import User
from django.http import HttpResponseForbidden

from wayapp.models import Note


def pilgrim_ownership_required(func):
    def decorated(request, *args, **kwargs):
        pilgrim = Note.objects.get(pk=kwargs['pk'])
        if not pilgrim.writer == request.user:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated