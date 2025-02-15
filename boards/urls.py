from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BoardViewSet, ColumnViewSet, TeamMemberViewSet

router = DefaultRouter()
router.register(r'boards', BoardViewSet, basename='board')

urlpatterns = [
    path('', include(router.urls)),
    path('boards/<uuid:board_pk>/columns/',
         ColumnViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='board-columns'),
    path('boards/<uuid:board_pk>/team-members/',
         TeamMemberViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='board-team-members'),
]
