from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Board
from .serializers import BoardSerializer


class BoardListView(APIView):
    """
    View for listing and creating boards.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve all boards.
        """
        boards = Board.objects.filter(
            created_by=request.user)
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new board.
        """
        serializer = BoardSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BoardDetailView(APIView):
    """
    View for retrieving, updating, and deleting a specific board.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper method to get a board by its primary key.
        """
        try:
            # Ensure the board belongs to the authenticated user
            return Board.objects.get(pk=pk, created_by=self.request.user)
        except Board.DoesNotExist:
            return None

    def get(self, request, pk):
        """
        Retrieve a specific board.
        """
        board = self.get_object(pk)
        if not board:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = BoardSerializer(board)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a specific board.
        """
        board = self.get_object(pk)
        if not board:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = BoardSerializer(board, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a specific board.
        """
        board = self.get_object(pk)
        if not board:
            return Response(status=status.HTTP_404_NOT_FOUND)
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
