from django.urls import path

from commentapp.views import CommentCreateView, CommentDeleteView

app_name = "commentapp"

urlpatterns = [
    path('create/', CommentCreateView, name='create'),
    path('delete/<int:pk>', CommentDeleteView, name='delete'),
]