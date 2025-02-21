from django.contrib import admin
from django.urls import path

from .views import FindOneTodoView, CreateTodoView, LoginView, SignUpView, FindAllTodoView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('login/', LoginView.as_view(), name='login'),
    path('todos/<int:pk>/', FindOneTodoView.as_view(), name='get_todo'),
    path('todos/', FindAllTodoView.as_view(), name='get_all_todo'),
    path('todos/', CreateTodoView.as_view(), name='create_todo'),
]