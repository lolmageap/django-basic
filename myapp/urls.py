from xml.etree.ElementInclude import include
from django.urls import path, include
from django.contrib import admin
from django.urls import path
from users.urls import router as user_router
from todos.urls import router as todo_router
from common.hybridrouter import HybridRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

router = HybridRouter()
router.register_router(user_router)
router.register_router(todo_router)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('api/', include(router.urls)),
]
