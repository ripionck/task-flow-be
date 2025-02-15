from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserRegistrationViewSet,
    CustomTokenObtainPairView,
    UserProfileViewSet,
    UserSettingsViewSet
)

router = DefaultRouter()
router.register(r'register', UserRegistrationViewSet, basename='register')

user_profile_viewset = UserProfileViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
})

user_settings_viewset = UserSettingsViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
})

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', user_profile_viewset, name='profile'),
    path('settings/', user_settings_viewset, name='settings'),
]
