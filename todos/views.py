from django.db import transaction
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Todos
from .serializers import CreateTodoSerializer, FindOneTodoResponseSerializer, FindAllTodoResponseSerializer, \
    FindAllTodoRequestSerializer


class CreateTodoView(CreateAPIView):
    serializer_class = CreateTodoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer = self.get_serializer(data=self.request.data)
        with transaction.atomic():
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Todo created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FindOneTodoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, pk: int):
        queryset = Todos.objects.filter(pk=pk)

        if not queryset.exists():
            return Response({"detail": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)

        response_serializer = FindOneTodoResponseSerializer(queryset.first())
        return Response(response_serializer.data, status=status.HTTP_200_OK)


class FindAllTodoView(ListAPIView):
    serializer_class = FindAllTodoResponseSerializer
    queryset = Todos.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        request_serializer = FindAllTodoRequestSerializer(data=self.request.query_params)
        request_serializer.is_valid(raise_exception=True)

        start_date = request_serializer.validated_data.get('start_date')
        end_date = request_serializer.validated_data.get('end_date')
        user = request_serializer.validated_data.get('user')
        is_completed = request_serializer.validated_data.get('is_completed')

        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        if user is not None:
            queryset = queryset.filter(user=user)
        if is_completed is not None:
            queryset = queryset.filter(is_completed=is_completed)

        return queryset
