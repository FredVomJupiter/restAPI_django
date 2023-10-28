from django.template.response import TemplateResponse
from django.shortcuts import render
from django.contrib.auth.models import User

from todo.models import Category, Contact, Subtask, Todo
from todo.serializers import CategorySerializer, ContactSerializer, SubtaskSerializer, TodoSerializer, UserSerializer

from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import BasicAuthentication, TokenAuthentication

from django.core.mail import EmailMessage


class TodoViewSet(viewsets.ModelViewSet):
    # API endpoint that allows todos to be viewed or edited.
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Todo.objects.all().order_by('-created_at')
    

    # cRud to list all todos for the current user
    def list(self, request, *args, **kwargs):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        # Get all todos for the current user
        queryset = Todo.objects.order_by('-created_at')
        serializer = TodoSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    

    # Crud to create a todo
    def create(self, request, *args, **kwargs):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            subtasks_data = serializer.validated_data.pop('subtasks', [])
            assigned_to_data = serializer.validated_data.pop('assigned_to', [])
            serializer.save(user=self.request.user)
            todo = serializer.instance

            for contact_id in assigned_to_data:
                todo.assigned_to.add(contact_id)
        
            for sub in subtasks_data:
                subtask = Subtask.objects.get(id=sub.id)
                subtask.todo = todo
                subtask.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    # crUd to update a todo
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.user_id != request.user.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = TodoSerializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def perform_update(self, serializer):
        assigned_to_data = serializer.validated_data.pop('assigned_to', None)
        instance = serializer.save()

        if assigned_to_data:
            instance.assigned_to.clear()
            for contact_id in assigned_to_data:
                instance.assigned_to.add(contact_id)
    

    # cruD to delete a todo
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user_id != request.user.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all().order_by('-name')


    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        queryset = Category.objects.order_by('-name')
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.user_id != request.user.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user_id != request.user.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContactViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Contact.objects.all().order_by('-name')


    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        queryset = Contact.objects.order_by('-name')
        serializer = ContactSerializer(queryset, many=True)
        return Response(serializer.data)
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.user_id != request.user.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user_id != request.user.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubtaskViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    serializer_class = SubtaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Subtask.objects.all().order_by('-title')


    def list(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        queryset = Subtask.objects.order_by('-title')
        serializer = SubtaskSerializer(queryset, many=True)
        return Response(serializer.data)
    

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)


    def update(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)
    

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LoginView(ObtainAuthToken):
    # API endpoint that allows users to login and receive a token.
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })
    

class LogoutView(APIView):
    # API endpoint that allows users to logout.
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        try:
            request.user.auth_token.delete()
        except Token.DoesNotExist:
            pass  # Token does not exist, so proceed without deleting
        return Response(data={'message': 'Logout successful'}, status=status.HTTP_200_OK)
    

class LoggedUserView(APIView):
    # API endpoint that allows users to get their own data.
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    

class RegisterView(APIView):
    # API endpoint that allows users to register.
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # No douplicat email
            if User.objects.filter(email=serializer.validated_data['email']).exists():
                return Response(data={'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            # Send verification email
            user = User.objects.get(email=serializer.validated_data['email'])
            user.is_active = False
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            email = EmailMessage(
                'Verify your account',
                'Click the link below to verify your account:\n\nhttp://127.0.0.1:8000/verify/' + token.key,
                to=[serializer.validated_data['email']]
            )
            email.send()
            return Response(data={'message': 'Registration successful'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeleteAccountView(APIView):
    # API endpoint that allows users to delete their account.
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs['pk'])
        if user.id != request.user.id:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user.delete()
        return Response(data={'message': 'Account deleted.'}, status=status.HTTP_200_OK)
    

class VerifyView(APIView):
    # API endpoint that allows users to verify their account.
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        if not Token.objects.filter(key=kwargs['token']).exists():
            # token does not exist
            response = TemplateResponse(request, 'verification_failed.html')
            return response
        token = Token.objects.get(key=kwargs['token'])
        user = User.objects.get(id=token.user_id)
        user.is_active = True
        user.save()
        # delete token
        token.delete()
        response = TemplateResponse(request, 'verify_email.html')
        return response