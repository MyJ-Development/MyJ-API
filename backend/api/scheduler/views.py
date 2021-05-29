import logging
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from ..auth.views import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
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

    @staticmethod
    def get(request):
        """ Obtener Clientes Por Rut
            Parametros
            
                {
                    "client_rut" : "RUTCLIENTE"
                }  
        """
        try:
            client = get_client_by_rut(request.GET.get('rut'))
        except:
            pass
        try:
            client = get_client_by_rut(request.data['rut'])
        except:
            pass


        serialize = ClientSerializer(client)
        return JsonResponse(serialize.data,safe=False)

    @staticmethod
    def put(request):
        """ Actualizar cliente
            Parametros
            // Se deben enviar todos los campos, aunque no se quiera modificar

                {

                    "rut":"9876543211",
                    "email":"asdas@asda.com",
                    "nombre":"testing",
                    "contacto1":"1231233",
                    "contacto2":"1231232",
                    "created_by": "test@test.test",
                    "updated_by": "test@test.test"
                }
        """
        data = common_methods.get_request_data(request)
        client = update_client(data)
        serialize = ClientSerializer(client)
        return JsonResponse(serialize.data,safe=False)
    
    @staticmethod
    def post(request):
        """ Agregar cliente
            //
                {

                    "rut":"987654321",
                    "email":"asdas@asda.com",
                    "nombre":"testing",
                    "contacto1":"1231233",
                    "contacto2":"1231232",
                    "created_by": "test@test.test",
                    "updated_by": "test@test.test"
                }
        """
        data = common_methods.get_request_data(request)
        client = get_client_by_rut(data['rut'])
        if(client):
            return JsonResponse({ "Code":"303" ,"Response": "Already exists"})
        else:
            client=create_client(data)
            serialize = ClientSerializer(client)
            return JsonResponse(serialize.data,safe=False)

class SchedulerResidenceView(APIView):

    @staticmethod
    def get(request):
        """ Obtener Residencias por rut de usuario
            Parametros
            
                {
                    "rut" : "RUTCLIENTE"
                }  
        """
        residence = ""
        try: 
            residence = get_residence_by_rut(request.data['rut'])
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
        """ Agregar residencia
            //

                {

                    "comuna":"Comuna",
                    "direccion":"direccion",
                    "mac":"mac",
                    "pppoe":"pppoe",
                    "client_rut": "123456789"
                }
        """
        data = common_methods.get_request_data(request)
        residence=create_residence(data)
        serialize = ResidenceSerializer(residence)
        return JsonResponse(serialize.data,safe=False)

    @staticmethod
    def put(request):
        """ Actualizar residencia
            // Se deben enviar todos los campos, aunque no se quiera modificar

                {
                    "id":"1"
                    "comuna":"Comuna",
                    "direccion":"direccion",
                    "mac":"mac",
                    "pppoe":"pppoe"
                }
        """
        data = common_methods.get_request_data(request)
        residence = update_residence(data)
        serialize = ResidenceSerializer(residence)
        return JsonResponse(serialize.data,safe=False)

class SchedulerTechnicianView(APIView):

    @staticmethod
    def get(request):
        """ Obtener todos los tecnicos
            Parametros
            
                {
                    "active":"1"  // (opcional)
                }  
        """
        #technician = get_technician_by_rut(request.GET.get('rut'))
        active = ''
        try:
            #active = request.data['active']
            active = request.GET.get('active')
        except:
            active = ''
        technician = get_technicians(active)
        serialize = TechnicianSerializer(technician,many=True)
        return JsonResponse(serialize.data,safe=False)
    
    @staticmethod
    def post(request):
        """ Agregar tecnico
            //

                {

                    "comuna":"Comuna",
                    "rut":"123456789",
                    "nombre":"nombre",
                    "capacidad":"7",
                    "estado":"No disponible"
                }
        """

        data = common_methods.get_request_data(request)
        technician=create_technician(data)
        serialize = TechnicianSerializer(technician)
        return JsonResponse({"Code":"200"},safe=False)

    @staticmethod
    def put(request):
        """ Actualizar tecnico
            // Se deben enviar todos los campos, aunque no se quieran modificar

                {
                    "id" : "1",
                    "comuna" : "comuna",
                    "nombre" : "nombre",
                    "capacidad" : "10",
                    "estado" : "Vacaciones",
                    "rut" : "12345689-0",
                    "active" : "0"
                }
        """
        data = common_methods.get_request_data(request)
        technician = update_technician(data)
        serialize = TechnicianSerializer(technician)
        return JsonResponse(serialize.data,safe=False)

class SchedulerOrderView(APIView):

    @staticmethod
    def get(request):
        """ Obtener order por rangos de fecha. formato YYYY-MM-DD
            Parametros
            
                {
                    "date_init" : "2018-01-01",
                    "date_end" : "2021-01-01"
                }  
        """
        valid = 0
        try: 
            valid = request.GET.get('date_init')
            valid = request.GET.get('date_end')
            valid = 1
        except:
            valid = 0
        if(valid):
            order = get_order_by_date(request.GET.get('date_init'),request.GET.get('date_end'))

        serialize = OrderSerializer(order,many=True)
        return JsonResponse(serialize.data,safe=False)
    
    @staticmethod
    def post(request):
        """ Agregar orden
            //

                {

                    "id" : "40",
                    "idtipo" : "1",            
                    "prioridad" : "Primera del dia",
                    "disponibilidad" : "despues 10 am",
                    "comentario" : "comentarioo",
                    "fechaejecucion" : "2020-05-3",
                    "estadocliente" :  "1",
                    "estadoticket" :  "1",
                    "mediodepago" :  "Imported",
                    "monto" :  "0",
                    "created_by" : "test@test.test", 
                    "encargado" : "SINRUT2",  
                    "client_order" :  "7990228-4",
                    "domicilio" :  "1"
                }
        """

        data = common_methods.get_request_data(request)
        order=create_order(data)
        serialize = OrderSerializer(order)
        return JsonResponse(serialize.data,safe=False)

    @staticmethod
    def put(request):
        """ Actualizar orden
            // Se deben enviar todos los campos, aunque no se quiera modificar

                {

                    "id" : "40",
                    "idtipo" : "1",            
                    "prioridad" : "Primera del dia",
                    "disponibilidad" : "despues 10 am",
                    "comentario" : "comentarioo",
                    "fechaejecucion" : "2020-05-3",
                    "estadocliente" :  "1",
                    "estadoticket" :  "1",
                    "mediodepago" :  "Imported",
                    "monto" :  "0",
                    "created_by" : "test@test.test", 
                    "encargado" : "SINRUT2",  
                    "client_order" :  "7990228-4",
                    "domicilio" :  "1"
                }
        """
        data = common_methods.get_request_data(request)
        order = update_order(data)
        serialize = OrderSerializer(order)
        return JsonResponse(serialize.data,safe=False)

class SchedulerOrderTypeView(APIView):

    @staticmethod
    def get(request):
        """ Obtener Tipos de ordenes
            Parametros
            
                {
                    "active":"1"  // (opcional)
                }  
        """
        active = ''
        try:
            #active = request.data['active']
            active = request.GET.get('active')
        except:
            active = ''
        ordertype=get_ordertypes(active)
        serialize = OrderTypeSerializer(ordertype,many=True)
        return JsonResponse(serialize.data,safe=False)
    
    @staticmethod
    def post(request):
        """ Agregar tipo de orden
            Parametros
            
                {
                    "descripcion" : "Nuevo tipo de orden",
                    "peso" : "3",
                    "valor" : "1"
                }  
        """
        data = common_methods.get_request_data(request)
        ordertype=create_ordertype(data)
        serialize = OrderTypeSerializer(ordertype)
        return JsonResponse(serialize.data,safe=False)

    @staticmethod
    def put(request):
        """ Actualizar tipo de orden
            // Se deben enviar todos los campos, aunque no se quiera modificar

                {
                    "id" : "1",
                    "descripcion" : "descripcion",
                    "peso" : "5",
                    "valor" : "1",
                    "active" : "0"
                }
        """
        data = common_methods.get_request_data(request)
        typeorder = update_typeorder(data)
        serialize = OrderTypeSerializer(typeorder)
        return JsonResponse(serialize.data,safe=False)


    @staticmethod
    def index(request):        
        ordertype = get_ordertype_by_id(request.data['idtipo'])
        serialize = OrderTypeSerializer(ordertype)
        return JsonResponse(serialize.data,safe=False)

class SchedulerClientStatusView(APIView):

    @staticmethod
    def get(request):
        """ Obtener Estados de cliente
            Parametros
            
                {
                    "active":"1"  // (opcional)
                }  
        """
        active = ''
        try:
            #active = request.data['active']
            active = request.GET.get('active')
        except:
            active = ''
        ClientStatus=get_clientstatus(active)
        serialize = ClientStatusSerializer(ClientStatus,many=True)
        return JsonResponse(serialize.data,safe=False)
    
    @staticmethod
    def post(request):
        """ Agregar Estado de cliente
            Parametros
            
                {
                    "descripcion" : "Nuevo tipo de orden"
                }  
        """
        data = common_methods.get_request_data(request)
        ClientStatus=create_clientstatus(data)
        serialize = ClientStatusSerializer(ClientStatus)
        return JsonResponse(serialize.data,safe=False)

    @staticmethod
    def put(request):
        """ Actualizar estado cliente
            // Se deben enviar todos los campos, aunque no se quiera modificar

                {
                    "id" : "1",
                    "descripcion" : "descripcion",
                    "active" : "1",
                }
        """
        data = common_methods.get_request_data(request)
        client = update_clientstatus(data)
        serialize = ClientStatusSerializer(client)
        return JsonResponse(serialize.data,safe=False)

class SchedulerTicketStatusView(APIView):

    @staticmethod
    def get(request):
        """ Obtener Estados de ticket
            Parametros
            
                {
                    "active":"1"  // (opcional)
                }  
        """
        active = ''
        try:
            #active = request.data['active']
            active = request.GET.get('active')
        except:
            active = ''
        TicketStatus=get_ticketstatus(active)
        serialize = TicketStatusSerializer(TicketStatus,many=True)
        return JsonResponse(serialize.data,safe=False)
    
    @staticmethod
    def post(request):
        """ Agregar Estado de ticket
            Parametros
            
                {
                    "descripcion" : "Nuevo tipo de ticket"
                }  
        """
        data = common_methods.get_request_data(request)
        TicketStatus=create_ticketstatus(data)
        serialize = TicketStatusSerializer(TicketStatus)
        return JsonResponse(serialize.data,safe=False)

    @staticmethod
    def put(request):
        """ Actualizar estado ticket
            // Se deben enviar todos los campos, aunque no se quiera modificar

                {
                    "id" : "1",
                    "descripcion" : "descripcion",
                    "active" : "1",
                }
        """
        data = common_methods.get_request_data(request)
        ticket = update_ticketstatus(data)
        serialize = TicketStatusSerializer(ticket)
        return JsonResponse(serialize.data,safe=False)

class OrderByClientView(APIView):
    @staticmethod
    def get(request):
        """ Obtener ordenes por [rut,id orden, nombre encargado, domicilio, created_by]
            Parametros
            
                {

                    "rut_cliente":"18839285-7", #id_orden #nombre_encargado #domicilio #created_by
                    "date_init":"2018-01-01",
                    "date_end":"2021-01-01"
                }
        """
        order = ""
        filter_rut_cliente = ""
        filter_id_orden = ""
        filter_nombre_encargado = ""
        filter_domicilio = ""
        filter_created_by = ""
        date_init = ""
        date_end = ""
        try:
            date_init = request.GET.get('date_init')
            date_end = request.GET.get('date_end')
            #date_init = request.data['date_init']
            #date_end = request.data['date_end']
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
            #filter_nombre_encargado = request.data['nombre_encargado']
            filter_nombre_encargado = request.GET.get('nombre_encargado')
        except:
            pass
        try:
            filter_domicilio = request.GET.get('domicilio')
        except:
            pass
        try:
            filter_created_by = request.GET.get('created_by')
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
        if (filter_created_by and date_init and date_end):
            order = get_order_by_created_by_filter(filter_created_by,date_init,date_end)
        elif(date_init and date_end):
            order = get_order_by_created_by_filter("",date_init,date_end)
        serialize = OrderSerializer(order,many=True)
        return JsonResponse(serialize.data,safe=False)

class SchedulerPrioridadView(APIView):

    @staticmethod
    def get(request):
        """ Obtener Prioridades
            Parametros
            
                {
                    "active":"1"  // (opcional)
                }  
        """
        active = ''
        try:
            #active = request.data['active']
            active = request.GET.get('active')
        except:
            active = ''
        Prioridad=get_prioridades(active)
        serialize = PrioridadSerializer(Prioridad,many=True)
        return JsonResponse(serialize.data,safe=False)
    
    @staticmethod
    def post(request):
        """ Agregar Prioridad
            Parametros
            
                {
                    "descripcion" : "Nuevo tipo de prioridad"
                }  
        """
        data = common_methods.get_request_data(request)
        Prioridades=create_prioridad(data)
        serialize = PrioridadSerializer(Prioridades)
        return JsonResponse(serialize.data,safe=False)

    @staticmethod
    def put(request):
        """ Actualizar prioridad
            // Se deben enviar todos los campos, aunque no se quiera modificar

                {
                    "id" : "1",
                    "descripcion" : "descripcion",
                    "active" : "1",
                }
        """
        data = common_methods.get_request_data(request)
        prioridad = update_prioridad(data)
        serialize = PrioridadSerializer(prioridad)
        return JsonResponse(serialize.data,safe=False)

class SchedulerMedioDePagoView(APIView):

    @staticmethod
    def get(request):
        """ Obtener Medios de pago
            Parametros
            
                {
                    "active":"1"  // (opcional)
                }  
        """
        active = ''
        try:
            #active = request.data['active']
            active = request.GET.get('active')
        except:
            active = ''
        mediodepago=get_mediosdepago(active)
        serialize = MedioDePagoSerializer(mediodepago,many=True)
        return JsonResponse(serialize.data,safe=False)
    
    @staticmethod
    def post(request):
        """ Agregar medio de pago
            Parametros
            
                {
                    "descripcion" : "Nuevo tipo de medio de pago"
                }  
        """
        data = common_methods.get_request_data(request)
        mediodepago=create_mediodepago(data)
        serialize = MedioDePagoSerializer(mediodepago)
        return JsonResponse(serialize.data,safe=False)

    @staticmethod
    def put(request):
        """ Actualizar medio de pago
            // Se deben enviar todos los campos, aunque no se quiera modificar

                {
                    "id" : "1",
                    "descripcion" : "descripcion",
                    "active" : "1",
                }
        """
        data = common_methods.get_request_data(request)
        mediodepago = update_mediodepago(data)
        serialize = MedioDePagoSerializer(mediodepago)
        return JsonResponse(serialize.data,safe=False)


class SchedulerUserView(APIView):

    @staticmethod
    def get(request):
        """ Obtener Usuarios
            Parametros
            
                {
                    "active":"1"  // (opcional)
                }  
        """
        active = ''
        try:
            #active = request.data['active']
            active = request.GET.get('active')
        except:
            active = ''
        users=get_users(active)
        serialize = UserSerializer(users,many=True)
        return JsonResponse(serialize.data,safe=False)
    
    @staticmethod
    def post(request):
        """ Agregar usuario
            Parametros
            
                {
                        
                    "email" : "email@email.email",
                    "password" : "password",
                    "name" : "name",
                    "rut" : "rut",
                    "role" : "role"
                }
        """
        data = common_methods.get_request_data(request)
        usr=create_user(data)
        serialize = UserSerializer(usr)
        refresh = CustomTokenObtainPairSerializer.get_token(
            get_user_by_email(email=data['email']))
        return JsonResponse({'token': {
            'access_token': str(refresh.access_token),
            'expires_in': str(refresh.access_token.lifetime.seconds),
            'refresh_token': str(refresh)
        }})
        #return JsonResponse(serialize.data,safe=False)

    @staticmethod
    def put(request):
        """ Actualizar user
            // Se deben enviar todos los campos, aunque no se quiera modificar

                {
                        
                    "email" : "email@email.email",
                    "password" : "password",
                    "name" : "name",
                    "rut" : "rut",
                    "role" : "role",
                    "active" : "0"
                }
        """
        data = common_methods.get_request_data(request)
        usr = update_user(data)
        serialize = UserSerializer(usr)
        return JsonResponse(serialize.data,safe=False)

class SchedulerTrackingView(APIView):

    @staticmethod
    def get(request):
        """ Obtener Seguimientos por id de orden 
            Parametros
            
                {
                    "order_id":"1"
                }  
        """
        tracks=get_tracking_by_order_id(request.GET.get('order_id'))
        serialize = TrackingSerializer(tracks,many=True)
        return JsonResponse(serialize.data,safe=False)
    
    @staticmethod
    def post(request):
        """ Agregar seguimiento a orden
            Parametros
            
                {
                        
                    "comentario" : "Seguimiento 1",
                    "user_email" : "test@test.test",
                    "order_id" : "1"
                }
        """
        data = common_methods.get_request_data(request)
        track=create_tracking(data)
        serialize = TrackingSerializer(track)
        return JsonResponse(serialize.data,safe=False)

class SchedulerTechOrderView(APIView):

    @staticmethod
    def get(request):
        """ Obtener tecnicos que realizan X tipo de orden
            Parametros
            
                {
                    "ordertype_id":"1", (Opcional)
                    "rut_tecnico":"12345678-9" (Opcional)
                }
        """
        try: 
            techs=get_techorder_by_ordertype_id(request.GET.get('ordertype_id'))
        except:
            pass

        try: 
            techs=get_techorder_by_tech_rut(request.GET.get('rut_tecnico'))
        except:
            pass   
        #techs=get_techorder_by_ordertype_id(request.data['ordertype_id'])
        serialize = TechnicianSerializer(techs,many=True)
        return JsonResponse(serialize.data,safe=False)
    
    @staticmethod
    def post(request):
        """ Agregar tipo de orden a tecnico
            Parametros
            
                {
                        
                    "ordertype_id" : "1",
                    "tecnico_rut" : "12345678-9"
                }
        """
        data = common_methods.get_request_data(request)
        techorder=create_techordertype(data)
        serialize = TechnicianSerializer(techorder)
        return JsonResponse(serialize.data,safe=False)

    @staticmethod
    def put(request):
        """ Eliminar tipo de orden a tecnico
            Parametros
            
                {
                        
                    "ordertype_id" : "1",
                    "tecnico_rut" : "12345678-9"
                }
        """
        data = common_methods.get_request_data(request)
        techorder=delete_techordertype(data)
        serialize = TechnicianSerializer(techorder)
        return JsonResponse(serialize.data,safe=False)

class SchedulerUserAssignedTechView(APIView):

    @staticmethod
    def get(request):
        """ Obtener tecnicos que tiene asignado un vendedor
            Parametros
            
                {
                    "user_email":"test@test.test", (Opcional)
                    "rut_tecnico":"12345678-9" (Opcional)
                }
        """
        raise Exception(request.GET.get('user_email'))
        try: 
            techs=get_user_assigned_tech_by_user_email(request.GET.get('user_email'))
        except:
            pass

        try: 
            techs=get_user_assigned_tech_by_tech_rut(request.GET.get('rut_tecnico'))
        except:
            pass   
        #techs=get_techorder_by_ordertype_id(request.data['ordertype_id'])
        serialize = TechnicianSerializer(techs,many=True)
        return JsonResponse(serialize.data,safe=False)
    
    @staticmethod
    def post(request):
        """ Agregar tecnico a un vendedor
            Parametros
            
                {
                        
                    "user_email":"test@test.test",
                    "tecnico_rut" : "12345678-9"
                }
        """
        data = common_methods.get_request_data(request)
        techorder=create_user_assigned_tech(data)
        serialize = TechnicianSerializer(techorder)
        return JsonResponse(serialize.data,safe=False)

    @staticmethod
    def put(request):
        """ Eliminar tecnico a vendedor
            Parametros
            
                {
                        
                    "user_email":"test@test.test",
                    "tecnico_rut" : "12345678-9"
                }
        """
        data = common_methods.get_request_data(request)
        techorder=delete_user_assigned_tech(data)
        serialize = TechnicianSerializer(techorder)
        return JsonResponse(serialize.data,safe=False)
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['role'] = user.role

        return token

class SchedulerOrderCheckerView(APIView):

    @staticmethod
    def get(request):
        """ Revisa si el cliente tiene ordenes abiertas o posee deuda (Esto ultimo pendiente)
            Parametros
            
                {
                    "rut_cliente":"12345678-9"
                }
        """

        valid = 0
        try:
            valid = get_orderchecker(request.GET.get('rut_cliente'))
        except:
            valid = 0

        if(not valid):
            try:
                valid = get_orderchecker(request.data['rut_cliente'])
            except:
                valid = 0
        #serialize = OrderSerializer(valid,many=True)
        return JsonResponse({"response":valid},safe=False)
        #return JsonResponse(serialize.data,safe=False)
