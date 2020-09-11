import logging
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from ..auth.views import CustomTokenObtainPairSerializer
from django.http import JsonResponse
from ..common import Common
from .controller import get_client_by_rut, update_client, create_client
from .controller import get_residence_by_rut,create_residence,get_residence_by_id
from .controller import get_technician_by_rut,create_technician
from .controller import get_user_by_email
from .controller import create_order,get_order_by_id
from .serializers import ResidenceSerializer
from rest_framework import serializers
from django.http import HttpResponse
from django.http import JsonResponse
import json
from rest_framework.renderers import JSONRenderer

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
            client=create_client(data)
            return JsonResponse(_serialize_client(client))

class SchedulerResidenceView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        residence = get_residence_by_rut(request.data['rut'])
        serialize = ResidenceSerializer(residence,many=True)
        return JsonResponse(serialize.data,safe=False)

    @staticmethod
    def post(request):
        data = common_methods.get_request_data(request)
        residence=create_residence(data)
        return JsonResponse(_serialize_residence(residence))

class SchedulerTechnicianView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        technician = get_technician_by_rut(request.data['rut'])
        return JsonResponse(_serialize_technician(technician))
    
    @staticmethod
    def post(request):
        data = common_methods.get_request_data(request)
        technician=create_technician(data)
        return JsonResponse(_serialize_technician(technician))

class SchedulerOrderView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        order = get_order_by_date(request.data['date'])
        serialize = OrderSerializer(order,many=True)
        return JsonResponse(serialize.data,safe=False)
    
    @staticmethod
    def post(request):
        data = common_methods.get_request_data(request)
        order=create_order(data)
        return JsonResponse(_serialize_order(order))


def _serialize_client(client):
    return {
        "Code":"200",
        "Response": {
            'email': client.email,
            'rut': client.rut,
            'contacto1': client.contacto1,
            'contacto2': client.contacto2,
            'created_at' : client.created_at,
            'updated_at' : client.updated_at
        }
    }

def _serialize_residence(residence):
    return {
        "Code":"200",
        "Response": {
            'id': residence.id,
            'comuna': residence.comuna,
            'direccion': residence.direccion,
            'mac': residence.mac,
            'pppoe': residence.pppoe
        }
    }


def _serialize_technician(technician):
    return {
        "Code":"200",
        "Response": {
            'rut': technician.rut,
            'comuna': technician.comuna,
            'nombre': technician.nombre,
            'estado': technician.estado,
            'capacidad': technician.capacidad
        }
    }

def _serialize_order(order):
    return {
        "Code":"200",
        "Response": {
            'id': order.id,
            'tipo': order.tipo,
            'prioridad': order.prioridad,
            'disponibilidad': order.disponibilidad,
            'comentario': order.comentario,
            'fechaejecucion': order.fechaejecucion,
            'estadocliente': order.estadocliente,
            'estadoticket': order.estadoticket,
            'mediodepago': order.mediodepago,
            'monto': order.monto,
            'created_at': order.created_at
        }
    }

