from django.urls import path
from django.views.generic import TemplateView

app_name = "pilgrimsapp"

urlpatterns = [
    path('intro/', TemplateView.as_view(template_name='pilgrimsapp/intro.html'), name='intro'),
]