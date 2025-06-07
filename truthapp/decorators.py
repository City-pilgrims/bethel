from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from truthapp.models import RecitingBoard

def reciting_ownership_required(func):
    def decorated(request, *args, **kwargs):
        reciting = get_object_or_404(RecitingBoard, pk=kwargs['pk'])
        if not reciting.author == request.user:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated