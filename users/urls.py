from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserProfileView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    # path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),
]
