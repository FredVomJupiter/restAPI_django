from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, Contact, Priority, Subtask, Todo

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'color']


class SubtaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Subtask
        fields = ['id', 'title', 'completed']


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'phone', 'user']


class PrioritySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Priority
        fields = ['id', 'name']


class TodoSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all(), many=True)
    subtask = SubtaskSerializer(many=True, required=False)
    priority = serializers.PrimaryKeyRelatedField(queryset=Priority.objects.all())

    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'completed', 'created_at', 'user', 'category', 'priority', 'due_date', 'assigned_to', 'subtask']
    
    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtask', [])
        assigned_to_data = validated_data.pop('assigned_to', [])
        todo = Todo.objects.create(**validated_data)

        for subtask_data in subtasks_data:
            Subtask.objects.create(todo=todo, **subtask_data)

        for contact_id in assigned_to_data:
            todo.assigned_to.add(contact_id)

        return todo