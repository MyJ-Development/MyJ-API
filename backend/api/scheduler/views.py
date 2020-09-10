import logging
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from ..auth.views import CustomTokenObtainPairSerializer
from django.http import JsonResponse
from ..common import Common
from .controller import get_client_by_rut, update_client, create_client

logger = logging.getLogger(__name__)
common_methods = Common()


class SchedulerClientView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        client = get_client_by_rut(request.data['rut'])
        return JsonResponse(_serialize_client(client))

    @staticmethod
    def put(request):
        client = get_client_by_rut(request.client.rut)
        data = common_methods.get_request_data(request)
        client.email = data['email']
        client.first_name = data['firstName']
        client.last_name = data['lastName']
        client.login = data['login']
        client.age = data['age']
        client.street = data['address']['street']
        client.city = data['address']['city']
        client.zip = data['address']['zipCode']
        client.role = data['role']

        update_client(client)

        # generate new tokens because client's data inside prvious generated token is changed
        refresh = CustomTokenObtainPairSerializer.get_token(client)
        return JsonResponse( {
            'access_token': str(refresh.access_token),
            'expires_in': str(refresh.access_token.lifetime.seconds),
            'refresh_token': str(refresh)
        })
    
    @staticmethod
    def post(request):
        data = common_methods.get_request_data(request)
        client = get_client_by_rut(data['rut'])
        if(client):
            return JsonResponse({ "Code":"303" ,"Response": "Already exists"})
        else:
            client=create_client(data['rut'],data['nombre'],data['email'],data['contacto1'],data['contacto2'],data['created_by'],data['updated_by'])
            return JsonResponse(_serialize_client(client))


def _serialize_client(client):
    return {
        "Code":"200",
        "Response": {
            'email': client.email,
            'rut': client.rut,
            'contacto1': client.contacto1,
            'contacto2': client.contacto2,
            'created_by' : client.created_by,
            'updated_by' : client.updated_by,
            'created_at' : client.created_at,
            'updated_at' : client.updated_at
        }
    }