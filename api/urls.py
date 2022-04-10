
from django.urls import path

from .views import UserViewSets, MatchView, ListView

app_name = "api"

urlpatterns = [
    path('clients/create/',UserViewSets.as_view({'post': 'create'}),name='create'),
    path('clients/<int:pk>/match/',MatchView.as_view({'post':'match'}),name='match'),
    path('list/', ListView.as_view(), name='list')
]


