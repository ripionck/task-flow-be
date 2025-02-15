from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Column
from .serializers import ColumnSerializer
from boards.models import Board


class ColumnListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve columns for boards owned by the authenticated user.
        """

        user_boards = Board.objects.filter(created_by=request.user)
        columns = Column.objects.filter(board__in=user_boards)
        serializer = ColumnSerializer(columns, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new column for a board owned by the authenticated user.
        """
        serializer = ColumnSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            # Set the creator to the authenticated user
            serializer.save(creator=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ColumnDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper method to get a column by its primary key.
        Ensure the column belongs to a board owned by the authenticated user.
        """
        try:
            column = Column.objects.get(pk=pk)
            if column.board.created_by != self.request.user:
                raise Column.DoesNotExist  # Prevent unauthorized access
            return column
        except Column.DoesNotExist:
            return None

    def get(self, request, pk):
        """
        Retrieve a specific column.
        """
        column = self.get_object(pk)
        if not column:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ColumnSerializer(column)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a specific column.
        """
        column = self.get_object(pk)
        if not column:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ColumnSerializer(
            column, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a specific column.
        """
        column = self.get_object(pk)
        if not column:
            return Response(status=status.HTTP_404_NOT_FOUND)
        column.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
