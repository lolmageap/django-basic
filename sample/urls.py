from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from sample.sample_detail_viewset import DetailViewSet
from sample.sample_viewset import SampleViewSet

router = DefaultRouter()
router.register(r'sample', SampleViewSet, basename='sample')

nested_router = NestedSimpleRouter(router, r'sample', lookup='sample')
nested_router.register(r'detail', DetailViewSet, basename='sample-detail')

urlpatterns = router.urls + nested_router.urls