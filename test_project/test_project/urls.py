from django.contrib import admin
from django.urls import path
from .views import GetPayPlansView, CreatePayPlanView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('payplan/<int:pk>/', GetPayPlansView.as_view(), name='get_payplan'),
    path('payplan/', CreatePayPlanView.as_view(), name='create_payplan'),
]
