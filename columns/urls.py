from django.urls import path
from . import views

urlpatterns = [
    path('', views.ColumnListView.as_view(), name='column-list'),
    path('<uuid:pk>/', views.ColumnDetailView.as_view(), name='column-detail'),
]
