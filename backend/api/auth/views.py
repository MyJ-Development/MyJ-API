import logging
from django.http import JsonResponse
from django.conf import settings

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.backends import TokenBackend

from ..common import Common
from ..user.controller import *
from ..models import User

logger = logging.getLogger(__name__)
common_methods = Common()
user_model = User()
ERROR_MSG = 'Can not authenticate with the given ' \
            'credentials or the account has been deactivated'


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['role'] = user.role

        return token


class AuthView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    @api_view(['POST'])
    def login(request):
        """ Iniciar Sesion
            Parametros
            
                {
                    "email" : "test@test.test",
                    "password" : "test"
                }  
        """
        logging.debug("Trying to login")
        data = common_methods.get_request_data(request)

        user = get_user_by_email(email=data['email'])

        if user:
            refresh = CustomTokenObtainPairSerializer.get_token(user)

            if check_password(user, data['password']):
                return JsonResponse({'token': {
                    'access_token': str(refresh.access_token),
                    'expires_in': str(refresh.access_token.lifetime.seconds),
                    'refresh_token': str(refresh)
                }})
            else:
                return JsonResponse({'message': 'Email or password incorrect'},
                                    status=status.HTTP_401_UNAUTHORIZED)
        return JsonResponse({'error': ERROR_MSG},
                            status=status.HTTP_403_FORBIDDEN)

    @staticmethod
    @api_view(['POST'])
    def sign_up(request):
        """ Registrar usuario
            Parametros
            
                {
                    "email" : "gabriel@myjchile.cl",
                    "password" : "123456",
                    "name" : "Gabriel Angael Ortega Jofre-(MAIPU)",
                    "rut" : "9744263345"
                }  
        """
        logging.debug("Trying to register a new user")
        data = common_methods.get_request_data(request)

        if check_user_exists(data['email']):
            return JsonResponse({'message': 'User with this email already exists'},
                                status=status.HTTP_400_BAD_REQUEST)

        create_user(data['email'], data['password'], data['name'],data['rut'])

        refresh = CustomTokenObtainPairSerializer.get_token(
            get_user_by_email(email=data['email']))
        return JsonResponse({'token': {
            'access_token': str(refresh.access_token),
            'expires_in': str(refresh.access_token.lifetime.seconds),
            'refresh_token': str(refresh)
        }})

    @staticmethod
    @api_view(['POST'])
    def request_pass(request):
        logging.debug("Trying to send password")
        email = common_methods.get_request_data(request)['email']

        try:
            send_password_reset_link(email)
        except ValueError as e:
            return JsonResponse({'message': str(e)},
                                status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({'message': 'Email was sent'},
                            status=status.HTTP_200_OK)

    @staticmethod
    @api_view(['POST'])
    def reset_pass(request):
        logging.debug("Trying to reset a password")
        data = common_methods.get_request_data(request)
        password = data['password']
        reset_password_token = data['reset_password_token']

        reset_user_password(reset_password_token, password)
        return JsonResponse({'message': 'Password reset successful'},
                            status=status.HTTP_200_OK)

    @staticmethod
    @api_view(['POST'])
    def sign_out(request):
        logging.debug("Trying to logout")
        return JsonResponse({'message': 'Logged out'},
                            status=status.HTTP_200_OK)

    @staticmethod
    @api_view(['POST'])
    def refresh_token(request):
        logging.debug("Trying to refresh token")

        data = common_methods.get_request_data(request)

        if not (data and data['token'] and data['token']['refresh_token']):
            return JsonResponse({'message': 'Invalid payload'},
                                status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh_token = str(data['token']['refresh_token'])
            token_decoder = TokenBackend(settings.SIMPLE_JWT['ALGORITHM'], settings.SIMPLE_JWT['SIGNING_KEY'])
            token_payload = token_decoder.decode(refresh_token)

            user = get_user_by_id(token_payload['user_id'])
            refresh = CustomTokenObtainPairSerializer.get_token(user)

            return JsonResponse({'token': {
                'access_token': str(refresh.access_token),
                'expires_in': str(refresh.access_token.lifetime.seconds),
                'refresh_token': str(refresh)
            }})
        except ValueError:
            return JsonResponse({'message': 'Invalid refresh token'},
                                status=status.HTTP_400_BAD_REQUEST)
