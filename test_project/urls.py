from django.contrib import admin
from django.urls import path
from .views import GetTodoView, CreateTodoView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('todos/<int:pk>/', GetTodoView.as_view(), name='get_todo'),
    path('todos/', CreateTodoView.as_view(), name='create_todo'),
]
