from common.hybridrouter import HybridRouter
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginView, SignUpView, LogoutView

router = HybridRouter()
router.add_api_view(r'sign-up', path('sign-up', SignUpView.as_view(), name='sign-up'))
router.add_api_view(r'login', path(r'login', LoginView.as_view(), name='login'))
router.add_api_view(r'logout', path(r'logout', LogoutView.as_view(), name='logout'))
router.add_api_view(r'refresh', path(r'refresh', TokenRefreshView.as_view(), name='refresh'))


urlpatterns = [
    path('', include(router.urls)),
]
