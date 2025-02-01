from django.urls import path
from django.views.generic import TemplateView

#from wayapp.views import PilgrimCreateView, PilgrimDetailView, PilgrimUpdateView, PilgrimDeleteView, PilgrimListView
from wayapp.views import NoteCreateView, NoteUpdateView, NoteDetailView, NoteListView, NoteDeleteView

app_name = "wayapp"

urlpatterns = [

    path('create/', NoteCreateView.as_view(), name='create'),
    path('update/<int:pk>', NoteUpdateView, name='update'),
    path('detail/<int:pk>', NoteDetailView.as_view(), name='detail'),
    path('delete/<int:pk>', NoteDeleteView, name='delete'),
    path('list/', NoteListView.as_view(), name='list'),
]