from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from .views import (
    CustomUserCreateView,
    MyTokenObtainPairView,
    get_user
)

urlpatterns = [
    path('register/', CustomUserCreateView.as_view(), name='register-user'),
    path('login/', MyTokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token-verify/', TokenVerifyView.as_view(), name='token-verify'),
    path('me/', get_user, name='get-user'),
]   