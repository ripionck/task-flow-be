from django.urls import path
from . import views

urlpatterns = [
    path('boards/', views.BoardListView.as_view(), name='board-list'),
    path('boards/<uuid:pk>/', views.BoardDetailView.as_view(), name='board-detail'),
]
