
from django.urls import path
from . import views

urlpatterns = [
    path('', views.CommentListView.as_view(), name='comment-list'),
    path('<uuid:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
]
