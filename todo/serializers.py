from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, Contact, Priority, Subtask, Todo

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
        fields = ['id', 'title', 'completed']


class ContactSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'phone', 'user']


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ['id', 'name']


class TodoSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    assigned_to = serializers.PrimaryKeyRelatedField(queryset=Contact.objects.all(), many=True)
    subtasks = SubtaskSerializer(many=True, required=False)
    priority = serializers.PrimaryKeyRelatedField(queryset=Priority.objects.all())

    class Meta:
        model = Todo
        fields = ['id', 'title', 'description', 'completed', 'created_at', 'user', 'category', 'priority', 'due_date', 'assigned_to', 'subtasks']
        read_only_fields = ['user', 'created_at']
    
    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks', None)
        assigned_to_data = validated_data.pop('assigned_to', None)
        todo = Todo.objects.create(**validated_data)

        if subtasks_data:
            for subtask_data in subtasks_data:
                Subtask.objects.create(todo=todo, **subtask_data)

        for contact_id in assigned_to_data:
            todo.assigned_to.add(contact_id)

        return todo
    

    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop('subtasks')
        assigned_to_data = validated_data.pop('assigned_to')
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.completed = validated_data.get('completed', instance.completed)
        instance.category = validated_data.get('category', instance.category)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.save()

        if assigned_to_data:
            instance.assigned_to.clear()
            for contact_id in assigned_to_data:
                instance.assigned_to.add(contact_id)

        # Get all subtasks with the todo id
        relevant_subtasks = Subtask.objects.filter(todo=instance)

        if subtasks_data:
            subtask_ids_from_data = [item.get('id') for item in subtasks_data if item.get('id') is not None]
    
            # Iterate through relevant_subtasks and update or delete as needed
            for subtask in relevant_subtasks:
                if subtask.id in subtask_ids_from_data:
                # Update existing subtask
                    sub_data = next((sub_data for sub_data in subtasks_data if sub_data.get('id') == subtask.id), None)
                    if sub_data:
                        subtask.title = sub_data.get('title', subtask.title)
                        subtask.completed = sub_data.get('completed', subtask.completed)
                        subtask.save()
            else:
                # Delete subtask that is no longer present in subtasks_data
                subtask.delete()

            for subtask_data in subtasks_data:
                if subtask_data.get('id') is None:
                    Subtask.objects.create(todo=instance, **subtask_data)

        return instance