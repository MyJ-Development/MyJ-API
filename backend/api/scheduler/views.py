import logging
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from ..auth.views import CustomTokenObtainPairSerializer
from django.http import JsonResponse
from ..common import Common
from .controller import *
from .serializers import *
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
        client = get_client_by_rut(request.GET.get('rut'))
        serialize = ClientSerializer(client)
        return JsonResponse(serialize.data,safe=False)

    @staticmethod
    def put(request):
        data = common_methods.get_request_data(request)
        client = update_client(data)
        serialize = ClientSerializer(client)
        return JsonResponse(serialize.data,safe=False)
    
    @staticmethod
    def post(request):
        data = common_methods.get_request_data(request)
        client = get_client_by_rut(data['rut'])
        if(client):
            return JsonResponse({ "Code":"303" ,"Response": "Already exists"})
        else:
            client=create_client(data)
            serialize = ClientSerializer(client)
            return JsonResponse(serialize.data,safe=False)

class SchedulerResidenceView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        residence = ""
        try: 
            residence = get_residence_by_rut(request.GET.get('rut'))
        except:
            residence = ""
            pass
        if(residence):
            pass
        else:
            residence = get_residence_by_rut(request.GET.get('rut'))
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
        #technician = get_technician_by_rut(request.GET.get('rut'))
        technician = get_technicians()
        serialize = TechnicianSerializer(technician,many=True)
        return JsonResponse(serialize.data,safe=False)
    
    @staticmethod
    def post(request):
        data = common_methods.get_request_data(request)
        technician=create_technician(data)
        return JsonResponse(_serialize_technician(technician))

class SchedulerOrderView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        order = get_order_by_date(request.GET.get('date_init'),request.GET.get('date_end'))
        serialize = OrderSerializer(order,many=True)
        return JsonResponse(serialize.data,safe=False)
    
    @staticmethod
    def post(request):
        data = common_methods.get_request_data(request)
        order=create_order(data)
        serialize = OrderSerializer(order)
        return JsonResponse(serialize.data,safe=False)

    @staticmethod
    def put(request):
        data = common_methods.get_request_data(request)
        order = update_order(data)
        serialize = OrderSerializer(order)
        return JsonResponse(serialize.data,safe=False)

class SchedulerOrderTypeView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request):
        ordertype=get_ordertypes()
        serialize = OrderTypeSerializer(ordertype,many=True)
        return JsonResponse(serialize.data,safe=False)
    
    @staticmethod
    def post(request):
        data = common_methods.get_request_data(request)
        ordertype=create_ordertype(data)
        serialize = OrderTypeSerializer(ordertype)
        return JsonResponse(serialize.data,safe=False)

    @staticmethod
    def index(request):        
        ordertype = get_ordertype_by_id(request.data['idtipo'])
        serialize = OrderTypeSerializer(ordertype)
        return JsonResponse(serialize.data,safe=False)


class OrderByClientView(APIView):
    
    @staticmethod
    def get(request):
        filter_rut_cliente = ""
        filter_id_orden = ""
        filter_nombre_encargado = ""
        date_init = ""
        date_end = ""
        try:
            date_init = request.GET.get('date_init')
            date_end = request.GET.get('date_end')
        except:
            pass
        try:
            filter_rut_cliente = request.GET.get('rut_cliente')
        except:
            pass
        try:
            filter_id_orden = request.GET.get('id_orden')
        except:
            pass
        try:
            filter_nombre_encargado = request.GET.get('nombre_encargado')
        except:
            pass
        try:
            filter_domicilio = request.GET.get('domicilio')
        except:
            pass
        
        if (filter_rut_cliente):
            order = get_order_by_rut_filter(filter_rut_cliente)
        if (filter_id_orden):
            order = get_order_by_id_orden_filter(filter_id_orden)
        if (filter_nombre_encargado):
            order = get_order_by_nombre_encargado_filter(filter_nombre_encargado,date_init,date_end)
        if (filter_domicilio):
            order = get_order_by_domicilio_filter(filter_domicilio,date_init,date_end)

        serialize = OrderSerializer(order,many=True)
        return JsonResponse(serialize.data,safe=False)



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

