from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Comment
from .serializers import CommentSerializer
from tasks.models import Task


class CommentListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve comments for tasks owned by the authenticated user.
        """
        # Filter tasks owned by the authenticated user
        user_tasks = Task.objects.filter(board__created_by=request.user)
        # Filter comments for these tasks
        comments = Comment.objects.filter(task__in=user_tasks)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new comment for a task owned by the authenticated user.
        """
        serializer = CommentSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            # Set the user making the comment
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper method to get a comment by its primary key.
        Ensure the comment belongs to a task owned by the authenticated user.
        """
        try:
            comment = Comment.objects.get(pk=pk)
            if comment.task.board.created_by != self.request.user:
                raise Comment.DoesNotExist  # Prevent unauthorized access
            return comment
        except Comment.DoesNotExist:
            return None

    def get(self, request, pk):
        """
        Retrieve a specific comment.
        """
        comment = self.get_object(pk)
        if not comment:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a specific comment.
        """
        comment = self.get_object(pk)
        if not comment:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(
            comment, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a specific comment.
        """
        comment = self.get_object(pk)
        if not comment:
            return Response(status=status.HTTP_404_NOT_FOUND)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
