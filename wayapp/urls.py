from django.urls import path

from wayapp.views import NoteCreateView, NoteUpdateView, NoteDetailView, NoteListView, NoteDeleteView, like_note, \
    SPadd_item, SPlist, SPdetail, SPindex, SPdelete, SPupdate_item, PILvideo_upload, PILvideo_list, PILvideo_delete

app_name = "wayapp"

urlpatterns = [

    path('create/', NoteCreateView.as_view(), name='create'),
    path('update/<int:pk>', NoteUpdateView, name='update'),
    path('detail/<int:pk>', NoteDetailView.as_view(), name='detail'),
    path('delete/<int:pk>', NoteDeleteView, name='delete'),
    path('list/', NoteListView.as_view(), name='list'),
    path('note/<int:pk>/like/', like_note, name='like_note'),
    path('spinx/', SPindex, name='spindex'),
    path('spadd/', SPadd_item, name='spadd_item'),
    path('splist/', SPlist, name='splist'),
    path('spdetail/<int:pk>', SPdetail, name='spdetail'),
    path('spupdate/<int:pk>', SPupdate_item, name='spupdate'),
    path('spdelete/<int:pk>', SPdelete, name='spdelete'),
    path('video/', PILvideo_upload, name='pilvideoupload'),
    path('videolist/', PILvideo_list, name='pilvideolist'),
    path('videodelete/<int:pk>', PILvideo_delete, name='pilvideodelete'),

]