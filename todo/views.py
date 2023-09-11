from django.shortcuts import render
from todo.models import Todo

from todo.serializers import TodoSerializer
from rest_framework import viewsets, permissions

# Create your views here.
class TodoViewSet(viewsets.ModelViewSet):
    # API endpoint that allows todos to be viewed or edited.
    queryset = Todo.objects.all().order_by('-created_at')
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
