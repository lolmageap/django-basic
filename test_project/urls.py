from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import FindOneTodoView, CreateTodoView, LoginView, SignUpView, FindAllTodoView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign-up/', SignUpView.as_view(), name='sign_up'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('refresh/', TokenRefreshView.as_view(), name='generate_refresh_token'),
    path('todos/<int:pk>/', FindOneTodoView.as_view(), name='get_todo'),
    path('todos/', FindAllTodoView.as_view(), name='get_all_todo'),
    path('todos/', CreateTodoView.as_view(), name='create_todo'),
]