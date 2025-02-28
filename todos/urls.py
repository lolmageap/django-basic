from django.urls import path, include, re_path
from common.hybridrouter import HybridRouter
from django.urls import path, re_path
from .views import (
    CreateTodoView,
    FindAllTodoView,
    FindOneTodoView,
    UpdateTodoView,
    DeleteTodoView,
)

router = HybridRouter()
router.add_api_view(r'todos', path('todos/', CreateTodoView.as_view(), name='create_todo'), methods=['POST'])
router.add_api_view(r'todos', path('todos/', FindAllTodoView.as_view(), name='get_todos'), methods=['GET'])
router.add_api_view(r'todos/<int:pk>/', path('todos/<int:pk>/', FindOneTodoView.as_view(), name='get_todo'), methods=['GET'])
router.add_api_view(r'todos/<int:pk>/', path('todos/<int:pk>/', UpdateTodoView.as_view(), name='update_todo'), methods=['PUT'])
router.add_api_view(r'todos/<int:pk>/', path('todos/<int:pk>/', DeleteTodoView.as_view(), name='delete_todo'), methods=['DELETE'])

urlpatterns = [
    path('', include(router.urls)),
]
