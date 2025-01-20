from rest_framework import generics
from .models import PayPlan
from .serializers import PayPlanSerializer


def perform_create(serializer: PayPlanSerializer) -> None:
    serializer.save()


class CreatePayPlanView(generics.CreateAPIView):
    queryset = PayPlan.objects.all()
    serializer_class = PayPlanSerializer


class GetPayPlansView(generics.RetrieveAPIView):
    queryset = PayPlan.objects.all()
    serializer_class = PayPlanSerializer
    lookup_field = 'pk'

