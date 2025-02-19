from django.contrib import admin
from django.urls import path

from .views import FindOneTodoView, CreateTodoView, LoginView, SignUpView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('todos/<long:pk>/', FindOneTodoView.as_view(), name='get_todo'),
    path('todos/', CreateTodoView.as_view(), name='create_todo'),
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('login/', LoginView.as_view(), name='login'),
]