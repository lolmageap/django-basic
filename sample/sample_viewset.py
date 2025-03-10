from rest_framework.viewsets import GenericViewSet


class SampleViewSet(GenericViewSet):
    def retrieve(self, request, pk=None):
        pass