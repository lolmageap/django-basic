from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginView, SignUpView, LogoutView

urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='generate_refresh_token'),
]
