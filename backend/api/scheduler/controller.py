from passlib.hash import django_pbkdf2_sha256 as handler
import time
from Crypto.Cipher import AES
from Crypto import Random
import json
import hashlib
from django.conf import settings
from ..models import *
import logging
from django.utils import timezone

encryptor = None

def get_user_by_email(email):
    if not email:
        raise Exception('No user email provided.')
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return 0

#CLIENT
def get_client_by_email(email):
    if not email:
        raise Exception('No client email provided.')
    try:
        client = Client.objects.get(email=email)
    except client.DoesNotExist:
        client = None

    return client

def get_client_by_rut(rut):
    if not rut:
        raise Exception('No client rut provided.')
    try:
        client = Client.objects.get(rut=rut)
    except Exception:
        client = None
    return client

def get_clients():
    try:
        client = Client.objects.all()
    except Exception:
        client = None
    return client
    
def update_client(client):
    client.objects.filter(rut=client.rut).update(email=client.email,
                rut=client.rut,
                nombre=client.nombre,
                contacto1=client.contacto1,
                contacto2=client.contacto2,
                updated_by=client.updated_by)
    client.save()

def create_client(client):
    user = get_user_by_email(client['created_by'])
    client = Client(
                rut=client['rut'], 
                nombre=client['nombre'],
                email=client['email'],
                contacto1=client['contacto1'],
                contacto2=client['contacto2'],
                created_by=user,
                updated_by=user)

    client.save()
    return client

def update_client(client):
    client_updated = Client.objects.get(rut=client['rut'])
    user = get_user_by_email(client['created_by'])
    client_updated.rut=client['rut']
    client_updated.nombre=client['nombre']
    client_updated.email=client['email']
    client_updated.contacto1=client['contacto1']
    client_updated.contacto2=client['contacto2']
    client_updated.created_by=user
    client_updated.updated_by=user
    client_updated.save()
    return client_updated

#Residence
def get_residence_by_rut(rut):
    if not rut:
        raise Exception('residence rut not provided.')
    try:
        residence = Residence.objects.filter(client__rut=rut)

    except Exception:
        raise Exception("Not found")

    return residence

def get_residence_by_id(idresidence):

    if not idresidence:
        raise Exception('residence id not provided.')
    try:
        residence = Residence.objects.get(id=idresidence)

    except Exception:
        raise Exception("Excepcion")

    return residence

def create_residence(residence):
    client=get_client_by_rut(residence['client_rut'])
    residence = Residence(
            comuna=residence['comuna'],
            direccion=residence['direccion'],
            mac=residence['mac'],
            pppoe=residence['pppoe'],
            client=client)
    residence.save()
    return residence

def update_residence(residence):
    residence_updated = Residence.objects.get(id=residence['id'])
    residence_updated.comuna=residence['comuna']
    residence_updated.direccion=residence['direccion']
    residence_updated.mac=residence['mac']
    residence_updated.pppoe=residence['pppoe']
    residence_updated.save()
    return residence_updated

#Technician
def get_technician_by_rut(rut):
    if not rut:
        raise Exception('No technician rut provided.')
    try:
        return Technician.objects.get(rut=rut)
    except Exception:
        return None

def get_technicians():
    try:
        return Technician.objects.all()
    except Exception:
        return None

def create_technician(technician):
    technician = Technician(
            rut=technician['rut'],
            comuna=technician['comuna'],
            nombre=technician['nombre'],
            estado=technician['estado'],
            capacidad=technician['capacidad'])
    technician.save()
    return technician


#Order
def get_order_by_id(id):
    if not id:
        raise Exception('order id not provided.')
    try:
        order = Order.objects.get(id=id)
    except order.DoesNotExist:
        order = None

    return order

def get_order_by_date(date_init,date_end):
    if not date_end:
        raise Exception('date_end not provided.')
    try:
        
        order = Order.objects.filter(fechaejecucion__range=[date_init,date_end]).order_by("fechaejecucion")
    except Exception:
        raise Exception("Not found")

    return order

def get_order_by_rut(rut):
    if not rut:
        raise Exception('rut not provided.')
    try:
        order = Order.objects.filter(client_order__rut__contains=rut)
    except Exception:
        raise Exception("Not found")
    return order

def get_order_by_rut_filter(rut):
    if not rut:
        raise Exception('rut not provided.')
    try:
        order = Order.objects.filter(client_order__rut__contains=rut)
    except Exception:
        raise Exception("Not found")
    return order

def get_order_by_id_orden_filter(id_orden):
    if not id_orden:
        raise Exception('id_orden not provided.')
    try:
        order = Order.objects.filter(id=id_orden)
    except Exception:
        raise Exception("Not found")
    return order

def get_order_by_nombre_encargado_filter(nombre_encargado,date_init,date_end):
    if not nombre_encargado and date_init and date_end:
        raise Exception('nombre_encargado | date_init | date_end not provided.')
    try:
        order = Order.objects.filter(fechaejecucion__range=[date_init,date_end],encargado__nombre__contains=nombre_encargado)
    except Exception:
        raise Exception("Not found")
    return order

def get_order_by_domicilio_filter(domicilio,date_init,date_end):
    
    if not domicilio:
        raise Exception('domicilio not provided.')
    if not date_init and date_end:
        try:
            order = Order.objects.filter(fechaejecucion__range=[date_init,date_end],client_residence__direccion__contains=domicilio)
        except Exception:
            raise Exception("Not found")
    else:
        try:
            order = Order.objects.filter(client_residence__direccion__contains=domicilio)
        except Exception:
            raise Exception("Not found")
    return order

def create_order(order):
    user = get_user_by_email(order['created_by'])
    cliente = get_client_by_rut(order['client_order'])
    tecnico = get_technician_by_rut(order['encargado'])
    domicilio = get_residence_by_id(order['domicilio'])
    ordertype = get_ordertype_by_id(order['idtipo'])

    order = Order(
            tipo=ordertype,
            prioridad=order['prioridad'],
            disponibilidad=order['disponibilidad'],
            comentario=order['comentario'],
            fechaejecucion=order['fechaejecucion'],
            estadocliente=order['estadocliente'],
            estadoticket=order['estadoticket'],
            mediodepago=order['mediodepago'],
            monto=order['monto'],
            created_by=user,
            encargado=tecnico,
            client_order=cliente,
            client_residence=domicilio)
        
    order.save()
    return order

def update_order(order):
    order_updated = Order.objects.get(id=order['id'])
    user = get_user_by_email(order['created_by'])
    cliente = get_client_by_rut(order['client_order'])
    tecnico = get_technician_by_rut(order['encargado'])
    domicilio = get_residence_by_id(order['domicilio'])
    ordertype = get_ordertype_by_id(order['idtipo'])
    order_updated.tipo=ordertype
    order_updated.prioridad=order['prioridad']
    order_updated.disponibilidad=order['disponibilidad']
    order_updated.comentario=order['comentario']
    order_updated.fechaejecucion=order['fechaejecucion']
    order_updated.estadocliente=order['estadocliente']
    order_updated.estadoticket=order['estadoticket']
    order_updated.mediodepago=order['mediodepago']
    order_updated.monto=order['monto']
    order_updated.created_by=user
    order_updated.encargado=tecnico
    order_updated.client_order=cliente
    order_updated.client_residence=domicilio
    order_updated.save()
    return order_updated

#Tracking
def get_tracking_by_rut(rut):
    if not rut:
        raise Exception('residence rut not provided.')
    try:
        tracking = Tracking.objects.all()

    except Exception:
        raise Exception("Not found")

    return tracking

def create_tracking(residence):
    client=get_client_by_rut(residence['client_rut'])
    residence = Residence(
            comuna=residence['comuna'],
            direccion=residence['direccion'],
            mac=residence['mac'],
            pppoe=residence['pppoe'],
            client=client)
    residence.save()
    return residence


#OrderType
def get_ordertype_by_id(id):
    if not id:
        raise Exception('ordertype id not provided.')
    try:
        ordertype = OrderType.objects.get(id=id)
    except Exception:
        raise Exception("Not found")
    return ordertype

def get_ordertypes():
    try:
        ordertype = OrderType.objects.filter()
    except Exception:
        raise Exception("Not found")

    return ordertype

def create_ordertype(ordertype):
    ordertype = OrderType(
            descripcion=ordertype['descripcion'])
    ordertype.save()
    return ordertype


