from django.urls import path

from .views import FindOneTodoView, CreateTodoView, FindAllTodoView

urlpatterns = [
    path('todos/<int:pk>/', FindOneTodoView.as_view(), name='get_todo'),
    path('todos/', FindAllTodoView.as_view(), name='get_all_todo'),
    path('todos/', CreateTodoView.as_view(), name='create_todo'),
]
