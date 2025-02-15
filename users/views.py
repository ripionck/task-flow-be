from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer, UserProfileSerializer, UserSettingsSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, UserSettings


class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create the user
        user = serializer.save()

        # Create UserSettings for the new user
        UserSettings.objects.create(user=user)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class UserSettingsViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSettingsSerializer

    def get_object(self):
        return self.request.user.settings
