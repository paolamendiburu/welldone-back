from rest_framework import generics
from articles.serializers import UserSerializer
from articles.models import User
from articles.permissions import UserPermission
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from articles.models import Article
from articles.serializers import ArticleListSerializer, ArticleDetailSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.core.mail import send_mail

# class ArticleList(generics.ListCreateAPIView):
#     queryset = Article.objects.all()
#     permission_classes = (IsAuthenticated,)
#     serializer_class = ArticleListSerializer
#     lookup_field = 'uuid'
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#
# class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Article.objects.all()
#     permission_classes = (IsAuthenticated,)
#     serializer_class = ArticleDetailSerializer
#     lookup_field = 'uuid'
#
#
# class UserList(generics.ListAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (UserPermission,)
#
#
# class UserDetail(generics.RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'username': user.username,
            'id': user.pk,
            'token': token.key,
            'email': user.email,
            'first name:': user.first_name,
            'last_name:': user.last_name
        })


@api_view(["POST"])
@permission_classes((AllowAny,))
def recover_password(request):
    email = request.data.get("email")
    if email is None:
        return Response({'error': 'Please provide email'},
                        status=HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User not found'},
                        status=HTTP_404_NOT_FOUND)

    token, _ = Token.objects.get_or_create(user=user)
    id = str(user.id)
    send_mail(
        'Recuperar contraseña',
        user.username+' clica en el siguiente link: http://localhost:3000/update-password/'+token.key+'/'+id,
        'noreply@welldone.com',
        [email],
        fail_silently=False,
    )
    return Response({'status': 'send ok'},
                    status=HTTP_200_OK)
