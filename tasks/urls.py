from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('api/boards/<uuid:board_pk>/', include(router.urls)),
    path('api/tasks/<uuid:task_pk>/comments/',
         CommentViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='task-comments'),
]
