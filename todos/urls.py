from django.urls import path

from .views import FindOneTodoView, CreateTodoView, FindAllTodoView, UpdateTodoView, DeleteTodoView

urlpatterns = [
    path('todos/', CreateTodoView.as_view(), name='create_todo'),
    path('todos/', FindAllTodoView.as_view(), name='get_all_todo'),
    path('todos/<int:pk>/', FindOneTodoView.as_view(), name='get_todo'),
    path('todos/<int:pk>/', UpdateTodoView.as_view(), name='update_todo'),
    path('todos/<int:pk>/', DeleteTodoView.as_view(), name='delete_todo'),
]
