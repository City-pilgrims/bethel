from django.urls import path
from truthapp.views import index, bible

app_name = "truthapp"

urlpatterns = [
    path('index/', index, name='index'),
    path('bible/', bible, name='bible'),
]