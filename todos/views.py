from django.db import transaction
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Todos
from .serializers import CreateTodoSerializer, FindOneTodoResponseSerializer, FindAllTodoResponseSerializer, \
    FindAllTodoRequestSerializer, UpdateTodoSerializer


class CreateTodoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self):
        serializer = CreateTodoSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            serializer.save()
            return Response({"message": "Todo created successfully"}, status=status.HTTP_201_CREATED)


class FindOneTodoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, pk: int):
        queryset = Todos.objects.filter(pk=pk, user=self.request.user)

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
        queryset = self.queryset

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


class UpdateTodoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, pk: int):
        todo = Todos.objects.filter(pk=pk, user=self.request.user).first()
        if todo is None:
            return Response({"detail": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateTodoSerializer(data=self.request.data, instance=todo)
        serializer.is_valid(raise_exception=True)
        with transaction.atomic():
            serializer.save()
            return Response({"message": "Todo updated successfully"}, status=status.HTTP_200_OK)


class DeleteTodoView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, pk: int):
        todo = Todos.objects.filter(pk=pk, user=self.request.user).first()
        if todo is None:
            return Response({"detail": "Todo not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            todo.delete()
            return Response({"message": "Todo deleted successfully"}, status=status.HTTP_200_OK)
