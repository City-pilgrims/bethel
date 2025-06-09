from django.urls import path
from django.views.generic import TemplateView

from pilgrimsapp.views import intro_images, timeline_view, PilgrimBoardCreate, PilgrimBoardList, PilgrimBoardDelete, \
    PilgrimBoardUpdate, PilgrimBoardDetail, question_list, question_create, question_detail, question_update, \
    question_delete, secret_check, answer_create, answer_update, answer_delete

app_name = "pilgrimsapp"

urlpatterns = [
    path('intro/', intro_images, name='intro'),
    path('', timeline_view, name='timeline'),
    path('pilboard_create', PilgrimBoardCreate, name='pilboardcreate'),
    path('pilboard_list', PilgrimBoardList, name='pilboardlist'),
    path('pilboard_delete/<int:pk>', PilgrimBoardDelete, name='pilboarddelete'),
    path('pilboard_update/<int:pk>', PilgrimBoardUpdate, name='pilboardupdate'),
    path('pilboard_detail/<int:pk>', PilgrimBoardDetail, name='pilboarddetail'),

    path('question_list/', question_list, name='list'),
    path('question_create/', question_create, name='create'),
    path('question_detail/<int:pk>', question_detail, name='detail'),
    path('question_update/<int:pk>', question_update, name='update'),
    path('question_delete/<int:pk>', question_delete, name='delete'),

    # 비밀글 관련
    path('question_secret/<int:pk>', secret_check, name='secret_check'),

    # 답변 관련
    path('answer_create/<int:pk>', answer_create, name='answer_create'),
    path('<int:pk>/answer/<int:answer_pk>/update/', answer_update, name='answer_update'),
    path('<int:pk>/answer/<int:answer_pk>/delete/', answer_delete, name='answer_delete'),
]