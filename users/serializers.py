from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        view_name = "api-welldone:users-detail"
        fields = ['id', 'username', 'email']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'username': {
                'validators': [UniqueValidator(queryset=User.objects.all())]
            },
            'email': {
                'validators': [UniqueValidator(queryset=User.objects.all())]
            }
        }

    def create(self, validated_data):
        user = User()
        return self.update(user, validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username')
        instance.email = validated_data.get('email')
        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance

