from django.urls import path
from . import views

urlpatterns = [
    path('', views.BoardListView.as_view(), name='board-list'),
    path('<uuid:pk>/', views.BoardDetailView.as_view(), name='board-detail'),
]
