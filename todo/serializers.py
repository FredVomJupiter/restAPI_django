import json
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, Contact, Subtask, Todo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'color']


class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ['id', 'title', 'completed', 'todo']


class ContactSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'phone', 'user', 'color']


class TodoSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all(), many=True)
    subtasks = serializers.PrimaryKeyRelatedField(queryset=Subtask.objects.all(), many=True)

    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'status', 'created_at', 'user', 'category', 'priority', 'due_date', 'assigned_to', 'subtasks']
        read_only_fields = ['user', 'created_at']