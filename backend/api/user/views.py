import logging
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..auth.views import CustomTokenObtainPairSerializer
from django.http import JsonResponse

from ..common import Common
from .controller import get_user_by_id, update_user, \
    get_user_settings_by_id

logger = logging.getLogger(__name__)
common_methods = Common()


class UserView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        user = get_user_by_id(request.user.id)
        user.theme = get_user_settings_by_id(
            request.user.id).theme

        return JsonResponse(_serialize_user(user))

    @staticmethod
    def put(request):
        user = get_user_by_id(request.user.id)

        data = common_methods.get_request_data(request)
        user.email = data['email']
        user.first_name = data['firstName']
        user.last_name = data['lastName']
        user.login = data['login']
        user.age = data['age']
        user.street = data['address']['street']
        user.city = data['address']['city']
        user.zip = data['address']['zipCode']
        user.role = data['role']

        update_user(user)

        user.theme = get_user_settings_by_id(
            request.user.id).theme

        # generate new tokens because user's data inside prvious generated token is changed
        refresh = CustomTokenObtainPairSerializer.get_token(user)
        return JsonResponse( {
            'access_token': str(refresh.access_token),
            'expires_in': str(refresh.access_token.lifetime.seconds),
            'refresh_token': str(refresh)
        })


class UserSettings(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        user = get_user_settings_by_id(request.user.id)

        return JsonResponse({'themeName': user.theme})

    @staticmethod
    def put(request):
        user_settings = get_user_settings_by_id(request.user.id)

        user_settings.theme = common_methods.get_request_data(
            request)['themeName']
        user_settings.save()

        return JsonResponse({'message': 'User theme was updated'},
                            status=status.HTTP_200_OK)


def _serialize_user(user):
    return {
        'id': user.id,
        'email': user.email,
        'name': user.name,
        'rut': user.rut,
        'login': user.login,
        'role': user.role,
        'settings': {
            'themeName': user.theme
        }
    }
