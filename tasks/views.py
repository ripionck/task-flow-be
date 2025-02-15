from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Task
from .serializers import TaskSerializer
from boards.models import Board


class TaskListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve tasks for boards or columns owned by the authenticated user.
        """
        # Filter boards owned by the authenticated user
        user_boards = Board.objects.filter(created_by=request.user)
        tasks = Task.objects.filter(board__in=user_boards)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new task for a board or column owned by the authenticated user.
        """
        serializer = TaskSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            # Set the creator to the authenticated user
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper method to get a task by its primary key.
        Ensure the task belongs to a board or column owned by the authenticated user.
        """
        try:
            task = Task.objects.get(pk=pk)
            if task.board.created_by != self.request.user:
                raise Task.DoesNotExist  # Prevent unauthorized access
            return task
        except Task.DoesNotExist:
            return None

    def get(self, request, pk):
        """
        Retrieve a specific task.
        """
        task = self.get_object(pk)
        if not task:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a specific task.
        """
        task = self.get_object(pk)
        if not task:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(
            task, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a specific task.
        """
        task = self.get_object(pk)
        if not task:
            return Response(status=status.HTTP_404_NOT_FOUND)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
