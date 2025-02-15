from rest_framework import viewsets, permissions
from .models import Board, Column, TeamMember
from .serializers import BoardSerializer, ColumnSerializer, TeamMemberSerializer
from .permissions import IsBoardOwnerOrAdmin


class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated, IsBoardOwnerOrAdmin]

    def get_queryset(self):
        return Board.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        board = serializer.save(created_by=self.request.user)
        TeamMember.objects.create(
            user=self.request.user,
            board=board,
            role='owner'
        )


class ColumnViewSet(viewsets.ModelViewSet):
    serializer_class = ColumnSerializer
    permission_classes = [permissions.IsAuthenticated, IsBoardOwnerOrAdmin]

    def get_queryset(self):
        return Column.objects.filter(board_id=self.kwargs['board_pk'])

    def perform_create(self, serializer):
        serializer.save(board_id=self.kwargs['board_pk'])


class TeamMemberViewSet(viewsets.ModelViewSet):
    serializer_class = TeamMemberSerializer
    permission_classes = [permissions.IsAuthenticated, IsBoardOwnerOrAdmin]

    def get_queryset(self):
        return TeamMember.objects.filter(board_id=self.kwargs['board_pk'])

    def perform_create(self, serializer):
        serializer.save(board_id=self.kwargs['board_pk'])
