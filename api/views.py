from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import ToDoSerializer, ToDoToggleCompleteSerializer, UserSerializer
from todo.models import ToDo
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ToDoListCreate(generics.ListCreateAPIView):

    serializer_class = ToDoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ToDo.objects.filter(user=user).order_by('-created')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ToDoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = ToDoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ToDo.objects.filter(user=user)


class ToDoToggleComplete(generics.UpdateAPIView):

    serializer_class = ToDoToggleCompleteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ToDo.objects.filter(user=user)

    def perform_update(self, serializer):
        serializer.instance.completed = not(serializer.instance.completed)
        serializer.save()


class Signup(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
            'token': token.key,
            'user_id': token.user_id,
            'username': token.user.username
        })