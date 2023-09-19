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
    subtask = serializers.PrimaryKeyRelatedField(queryset=Subtask.objects.all(), many=True, blank=True, null=True)
    priority = serializers.PrimaryKeyRelatedField(queryset=Priority.objects.all())

    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'completed', 'created_at', 'user', 'category', 'priority', 'due_date', 'assigned_to', 'subtask']
    
    #def create(self, validated_data):
     #   category_data = validated_data.pop('category')
      #  category = Category.objects.get(id=category_data.id)
       # todo = Todo.objects.create(category=category, **validated_data)
        #return todo