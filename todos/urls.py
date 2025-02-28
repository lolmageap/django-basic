from django.urls import path, include, re_path
from common.hybridrouter import HybridRouter
from django.urls import path
from rest_framework import routers
from .views import TodoViewSet

router = HybridRouter()
router.register(r'todos', TodoViewSet, basename='todos')

urlpatterns = router.urls