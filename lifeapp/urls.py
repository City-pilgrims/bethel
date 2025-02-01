from django.urls import path
from django.views.generic import TemplateView

app_name = "lifeapp"

urlpatterns = [
    path('list/', TemplateView.as_view(template_name='lifeapp/list.html'), name='list'),
]