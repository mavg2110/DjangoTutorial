from rest_framework import serializers
from todo.models import ToDo
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class ToDoSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()
    completed = serializers.ReadOnlyField()

    class Meta:
        model = ToDo
        fields = ['id', 'title', 'memo', 'created', 'completed']


class ToDoToggleCompleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = ToDo
        fields = ['completed']


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user