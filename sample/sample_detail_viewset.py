from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

class DetailViewSet(GenericViewSet):
    permission_classes = [AllowAny]

    def list(self, request, sample_pk=None):
        return Response({"message": f"List of details for sample {sample_pk}"})

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="sample_pk",
                location=OpenApiParameter.PATH,
                description="Sample primary key",
                required=True,
                type=str
            ),
            OpenApiParameter(
                name="id",
                location=OpenApiParameter.PATH,
                description="Detail ID",
                required=True,
                type=str
            ),
        ]
    )
    def retrieve(self, request, sample_pk=None, pk=None):
        print(f"Sample PK: {sample_pk}")
        print(f"Detail PK: {pk}")
        return Response({"message": f"Detail {pk} of sample {sample_pk}"})
