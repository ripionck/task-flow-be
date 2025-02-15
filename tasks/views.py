from rest_framework import viewsets, permissions
from .models import Task, Comment
from .serializers import TaskSerializer, CommentSerializer
from boards.models import Board


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(board_id=self.kwargs['board_pk'])

    def perform_create(self, serializer):
        board = Board.objects.get(pk=self.kwargs['board_pk'])
        serializer.save(
            board=board,
            column=board.columns.first(),
            created_by=self.request.user
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['board'] = Board.objects.get(pk=self.kwargs['board_pk'])
        return context


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(task_id=self.kwargs['task_pk'])

    def perform_create(self, serializer):
        serializer.save(
            task_id=self.kwargs['task_pk'],
            user=self.request.user
        )
