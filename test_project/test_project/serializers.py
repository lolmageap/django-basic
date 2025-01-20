from rest_framework import serializers
from .models import PayPlan


class PayPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayPlan
        fields = '__all__'