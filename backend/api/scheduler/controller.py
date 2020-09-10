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

#CLIENT
def get_client_by_email(email):
    if not email:
        raise Exception('No client email provided.')
    try:
        client = Client.objects.get(email=email)
    except client.DoesNotExist:
        client = None

    return client

def get_client_by_id(id):
    if not id:
        raise Exception('No client id provided.')

    return Client.objects.get(id=id)

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

def create_client(rut,nombre,email,contacto1,contacto2,created_by,updated_by):
    client = {
        'rut':rut,
        'email':email,
        'contacto1':contacto1,
        'contacto2':contacto2,
        'created_by':created_by,
        'updated_by':updated_by
    }

    client = Client(email="hola",
                rut=rut,
                nombre=nombre,
                contacto1=contacto1,
                contacto2=contacto2,
                created_by="hola",
                updated_by=updated_by)

    client.save()
    return client

#Residence
def get_residence_by_email(email):
    if not email:
        raise Exception('residence email provided.')
    try:
        residence = Residence.objects.get(email=email)
    except residence.DoesNotExist:
        residence = None

    return residence

def create_residence(comuna,direccion,mac,pppoe,client_rut):
    client=get_client_by_rut(client_rut)
    residence = Residence(
            comuna=comuna,
            direccion=direccion,
            mac=mac,
            pppoe=pppoe,
            client=client)
    residence.save()
    return residence
