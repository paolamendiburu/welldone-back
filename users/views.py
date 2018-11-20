from django.core.mail import send_mail
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response


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
        user.username+' clica en el siguiente link: http://welldonecuatro.tk/update-password/'+token.key+'/'+id,
        'noreply@welldone.com',
        [email],
        fail_silently=False,
    )
    return Response({'status': 'send ok'},
                    status=HTTP_200_OK)
