from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationViewSet, CustomTokenObtainPairView, UserProfileViewSet, UserSettingsViewSet

router = DefaultRouter()
router.register(r'register', UserRegistrationViewSet, basename='register')
router.register(r'settings', UserSettingsViewSet, basename='settings')

user_profile_viewset = UserProfileViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
})

urlpatterns = [
    path('api/auth/', include(router.urls)),
    path('api/auth/token/', CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/auth/profile/', user_profile_viewset, name='profile'),
]
