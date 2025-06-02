from django.urls import path
from django.views.generic import TemplateView

from pilgrimsapp.views import intro_images, timeline_view, PilgrimBoardCreate, PilgrimBoardList, PilgrimBoardDelete, \
    PilgrimBoardUpdate, PilgrimBoardDetail

app_name = "pilgrimsapp"

urlpatterns = [
    path('intro/', intro_images, name='intro'),
    path('', timeline_view, name='timeline'),
    path('pilboard_create', PilgrimBoardCreate, name='pilboardcreate'),
    path('pilboard_list', PilgrimBoardList, name='pilboardlist'),
    path('pilboard_delete/<int:pk>', PilgrimBoardDelete, name='pilboarddelete'),
    path('pilboard_update/<int:pk>', PilgrimBoardUpdate, name='pilboardupdate'),
    path('pilboard_detail/<int:pk>', PilgrimBoardDetail, name='pilboarddetail'),
]