
from django.urls import path
from . import views

urlpatterns = [
    path('', views.TeamMemberListView.as_view(), name='team-member-list'),
    path('<uuid:pk>/', views.TeamMemberDetailView.as_view(),
         name='team-member-detail'),
]
