from django.contrib.auth.models import User
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from users.permissions import UserPermission
from users.serializers import UserSerializer, UserListSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [UserPermission]
    filter_backends = [SearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ['=username', '=email']
    filter_fields = ['username']
    ordering_fields = ['first_name']

    def get_serializer_class(self):

        if self.action == 'create' or self.action == 'update':
            return UserSerializer
        elif self.action == 'retrieve':
            return UserSerializer
        else:
            return UserListSerializer

