from django.urls import path
from truthapp.views import index, bible, RecitingListView, RecitingCreateView, RecitingDeleteView

app_name = "truthapp"

urlpatterns = [
    path('index/', index, name='index'),
    path('bible/', bible, name='bible'),
    path('recite_create/', RecitingCreateView.as_view(), name='create'),
    path('recite_list/', RecitingListView.as_view(), name='list'),
    path('recite_delete/<int:pk>/', RecitingDeleteView, name='delete'),
]