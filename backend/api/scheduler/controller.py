from passlib.hash import django_pbkdf2_sha256 as handler
import time
from Crypto.Cipher import AES
from Crypto import Random
import json
import hashlib
from django.conf import settings
from ..models import User, Client, Residence,Technician, Order, Tracking
import logging

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
        return Client.objects.get(rut=rut)
    except Exception:
        return 0
    
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
        raise Exception('residence rut provided.')
    try:
        residence = Residence.objects.get(rut=rut)
    except residence.DoesNotExist:
        residence = None

    return residence

def create_residence(residence):
    client=get_client_by_rut(residence['client_rut'])
    residence = Residence(
            comuna=residence['comuna'],
            direccion=residence['direccion'],
            mac=residence['mac'],
            pppoe=residence['pppoe'],
            client=residence['client'])
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
            rut=techinician['rut'],
            comuna=techinician['comuna'],
            nombre=techinician['nombre'],
            estado=techinician['estado'],
            capacidad=techinician['capacidad'])
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

def create_order(order):
    user = get_user_by_email(order['created_by'])
    cliente = get_client_by_rut(order['client_order'])
    tecnico = get_technician_by_rut(order['encargado'])

    order = Order(
            tipo=order['tipo'],
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
            client_order=cliente)
        
    order.save()
    return order