from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve notifications for the authenticated user.
        """
        notifications = Notification.objects.filter(user=request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new notification for the authenticated user.
        """
        serializer = NotificationSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            # Set the user to the authenticated user
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        """
        Helper method to get a notification by its primary key.
        Ensure the notification belongs to the authenticated user.
        """
        try:
            notification = Notification.objects.get(pk=pk)
            if notification.user != self.request.user:
                raise Notification.DoesNotExist  # Prevent unauthorized access
            return notification
        except Notification.DoesNotExist:
            return None

    def get(self, request, pk):
        """
        Retrieve a specific notification.
        """
        notification = self.get_object(pk)
        if not notification:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update a specific notification.
        """
        notification = self.get_object(pk)
        if not notification:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = NotificationSerializer(
            notification, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a specific notification.
        """
        notification = self.get_object(pk)
        if not notification:
            return Response(status=status.HTTP_404_NOT_FOUND)
        notification.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
