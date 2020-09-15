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

#Technician
def get_technician_by_rut(rut):
    if not rut:
        raise Exception('No technician rut provided.')
    try:
        return Technician.objects.get(rut=rut)
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

def get_order_by_date(date_end):
    if not date_end:
        raise Exception('order rut not provided.')
    try:
        order = Order.objects.filter(created_at__gte=timezone.now().date())

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

def create_ordertype(ordertype):
    ordertype = OrderType(
            descripcion=ordertype['descripcion'])
    ordertype.save()
    return ordertype


