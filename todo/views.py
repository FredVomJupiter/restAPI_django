from django.shortcuts import render
from todo.models import Todo

from todo.serializers import TodoSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

# Create your views here.
class TodoViewSet(viewsets.ModelViewSet):
    # API endpoint that allows todos to be viewed or edited.
    queryset = Todo.objects.all().order_by('-created_at')
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
