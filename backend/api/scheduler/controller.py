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
import datetime
from datetime import timedelta  
  
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
    old_rut = ''
    try:
        old_rut = client['old_rut']
        client_updated = Client.objects.get(rut=old_rut)
    except:
        client_updated = Client.objects.get(rut=client['rut'])

    if(old_rut):
        user = get_user_by_email(client['created_by'])
        client_updated.rut=client['rut']
        client_updated.nombre=client['nombre']
        client_updated.email=client['email']
        client_updated.contacto1=client['contacto1']
        client_updated.contacto2=client['contacto2']
        client_updated.created_by=user
        client_updated.updated_by=user
        client_updated.save()
        residence = Residence.objects.filter(client__rut=old_rut).update(client=client_updated)
        order = Order.objects.filter(client_order__rut=old_rut).update(client_order=client_updated)

    else:
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

def get_technicians(active):
    if(active):
        try:
            technicians = Technician.objects.filter(active=active)
        except Exception:
            raise Exception("Not found")
    else:
        try:
            technicians = Technician.objects.filter()
        except Exception:
            raise Exception("Not found")

    return technicians

def create_technician(technician):
    technician = Technician(
            rut=technician['rut'],
            comuna=technician['comuna'],
            nombre=technician['nombre'],
            estado=technician['estado'],
            capacidad=technician['capacidad'])
    technician.save()
    return technician

def update_technician(tech):
    technician_updated = Technician.objects.get(id=tech['id'])
    technician_updated.comuna=tech['comuna']
    technician_updated.nombre=tech['nombre']
    technician_updated.estado=tech['estado']
    technician_updated.rut=tech['rut']
    technician_updated.capacidad=tech['capacidad']
    technician_updated.active=tech['active']
    technician_updated.save()
    return technician_updated

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
        
        order = Order.objects.filter(fechaejecucion__range=[date_init,date_end]).order_by("-fechaejecucion")
    except Exception:
        raise Exception("Not found")

    return order

def get_order_by_rut(rut):
    if not rut:
        raise Exception('rut not provided.')
    try:
        order = Order.objects.filter(client_order__rut__contains=rut).order_by("-fechaejecucion")
    except Exception:
        raise Exception("Not found")
    return order

def get_order_by_rut_filter(rut):
    if not rut:
        raise Exception('rut not provided.')
    try:
        order = Order.objects.filter(client_order__rut__contains=rut).order_by("-fechaejecucion")
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
    order = ""
    if not nombre_encargado and date_init and date_end:
        raise Exception('nombre_encargado | date_init | date_end not provided.')
    try:
        order = Order.objects.filter(fechaejecucion__range=[date_init,date_end],encargado__nombre__contains=nombre_encargado).order_by("-fechaejecucion")

    except Exception:
        raise Exception("Not found")
    return order

def get_order_by_domicilio_filter(domicilio,date_init,date_end):
    if not domicilio:
        raise Exception('domicilio not provided.')
    if date_init and date_end:
        try:
            order = Order.objects.filter(fechaejecucion__range=[date_init,date_end],client_residence__direccion__contains=domicilio).order_by("fechaejecucion").order_by("-fechaejecucion")
        except Exception:
            raise Exception("Not found")
    else:
        try:
            order = Order.objects.filter(client_residence__direccion__contains=domicilio).order_by("-fechaejecucion")
        except Exception:
            raise Exception("Not found")
    return order

def get_order_by_created_by_filter(created_by,date_init,date_end):
    if date_init and date_end and created_by:
        try:
            order = Order.objects.filter(created_at__range=[date_init,date_end],created_by__email=created_by).order_by("-created_at")
        except Exception:
            pass
    elif date_init and date_end:
        try:
            order = Order.objects.filter(created_at__range=[date_init,date_end]).order_by("-created_at")
        except Exception:
            raise Exception("Not found")  

    return order

def create_order(order):
    user = get_user_by_email(order['created_by'])
    cliente = get_client_by_rut(order['client_order'])
    tecnico = get_technician_by_rut(order['encargado'])
    domicilio = get_residence_by_id(order['domicilio'])
    ordertype = get_ordertype_by_id(order['idtipo'])
    n_estadocliente=get_clientstatus_by_id(order['estadocliente'])
    n_estadoticket=get_ticketstatus_by_id(order['estadoticket'])
    n_prioridad=get_prioridad_by_id(order['prioridad'])
    n_mediodepago=get_mediodepago_by_id(order['mediodepago'])

    order = Order(
            tipo=ordertype,
            disponibilidad=order['disponibilidad'],
            comentario=order['comentario'],
            fechaejecucion=order['fechaejecucion'],
            monto=order['monto'],
            created_by=user,
            encargado=tecnico,
            client_order=cliente,
            client_residence=domicilio,
            estadocliente=n_estadocliente,
            estadoticket=n_estadoticket,
            prioridad=n_prioridad,
            mediodepago=n_mediodepago)
        
    order.save()
    return order

def update_order(order):
    order_updated = Order.objects.get(id=order['id'])
    user = get_user_by_email(order['created_by'])
    cliente = get_client_by_rut(order['client_order'])
    tecnico = get_technician_by_rut(order['encargado'])
    domicilio = get_residence_by_id(order['domicilio'])
    ordertype = get_ordertype_by_id(order['idtipo'])
    n_estadocliente=get_clientstatus_by_id(order['estadocliente'])
    n_estadoticket=get_ticketstatus_by_id(order['estadoticket'])
    n_prioridad=get_prioridad_by_id(order['prioridad'])
    n_mediodepago=get_mediodepago_by_id(order['mediodepago'])
    order_updated.tipo=ordertype
    order_updated.disponibilidad=order['disponibilidad']
    order_updated.comentario=order['comentario']
    order_updated.fechaejecucion=order['fechaejecucion']
    order_updated.monto=order['monto']
    order_updated.created_by=user
    order_updated.encargado=tecnico
    order_updated.estadocliente=n_estadocliente
    order_updated.estadoticket=n_estadoticket
    order_updated.prioridad=n_prioridad
    order_updated.mediodepago=n_mediodepago
    order_updated.client_order=cliente
    order_updated.client_residence=domicilio
    order_updated.save()
    return order_updated

#Tracking
def get_tracking_by_order_id(id):
    if not id:
        raise Exception('order id not provided.')
    try:
        tracking = Tracking.objects.filter(order_id=id)
    except Exception:
        raise Exception("Not found")
    return tracking

def create_tracking(tracking):
    user=get_user_by_email(tracking['user_email'])
    order=get_order_by_id(tracking['order_id'])
    new_tracking = Tracking(
            comentario=tracking['comentario'],
            created_by=user,
            order_id=order)
    new_tracking.save()
    return new_tracking



#OrderType
def get_ordertype_by_id(id):
    if not id:
        raise Exception('ordertype id not provided.')
    try:
        ordertype = OrderType.objects.get(id=id)
    except Exception:
        raise Exception("Not found")
    return ordertype

def get_ordertypes(active):
    if(active):
        try:
            ordertype = OrderType.objects.filter(active=active)
        except Exception:
            raise Exception("Not found")
    else:
        try:
            ordertype = OrderType.objects.filter()
        except Exception:
            raise Exception("Not found")

    return ordertype

def create_ordertype(ordertype):
    ordertype = OrderType(
            descripcion=ordertype['descripcion'],
            peso=ordertype['peso'],
            valor=ordertype['valor']
            )
    ordertype.save()
    return ordertype

def update_typeorder(typeorder):
    typeorder_updated = OrderType.objects.get(id=typeorder['id'])
    typeorder_updated.descripcion=typeorder['descripcion']
    typeorder_updated.active=typeorder['active']
    typeorder_updated.peso=typeorder['peso']
    typeorder_updated.valor=typeorder['valor']
    typeorder_updated.save()
    return typeorder_updated

#ClientStatus
def get_clientstatus_by_id(id):
    if not id:
        raise Exception('id not provided.')
    try:
        clientstat = ClientStatus.objects.get(id=id)
    except Exception:
        raise Exception("Not found")
    return clientstat

def get_clientstatus(active):
    if(active):
        try:
            clientstat = ClientStatus.objects.filter(active=active)
        except Exception:
            raise Exception("Not found")
    else:
        try:
            clientstat = ClientStatus.objects.filter()
        except Exception:
            raise Exception("Not found")

    return clientstat

def create_clientstatus(data):
    new_clientstatus = ClientStatus(descripcion=data['descripcion'])
    new_clientstatus.save()
    return new_clientstatus

def update_clientstatus(clientstat):
    client_updated = ClientStatus.objects.get(id=clientstat['id'])
    client_updated.descripcion=clientstat['descripcion']
    client_updated.active=clientstat['active']
    client_updated.save()
    return client_updated

#TicketStatus
def get_ticketstatus_by_id(id):
    if not id:
        raise Exception('id not provided.')
    try:
        ticketstat = TicketStatus.objects.get(id=id)
    except Exception:
        raise Exception("Not found")
    return ticketstat

def get_ticketstatus(active):
    if(active):
        try:
            ticketstat = TicketStatus.objects.filter(active=active)
        except Exception:
            raise Exception("Not found")
    else:
        try:
            ticketstat = TicketStatus.objects.filter()
        except Exception:
            raise Exception("Not found")

    return ticketstat

def create_ticketstatus(data):
    new_ticketstatus = TicketStatus(descripcion=data['descripcion'])
    new_ticketstatus.save()
    return new_ticketstatus

def update_ticketstatus(ticket):
    ticket_updated = TicketStatus.objects.get(id=ticket['id'])
    ticket_updated.descripcion=ticket['descripcion']
    ticket_updated.active=ticket['active']
    ticket_updated.save()
    return ticket_updated

#ClientStatus
def get_clientatus_by_id(id):
    if not id:
        raise Exception('id not provided.')
    try:
        clientstat = ClientStatus.objects.get(id=id)
    except Exception:
        raise Exception("Not found")
    return clientstat

def get_clientstatus(active):
    if(active):
        try:
            clientstat = ClientStatus.objects.filter(active=active)
        except Exception:
            raise Exception("Not found")
    else:
        try:
            clientstat = ClientStatus.objects.filter()
        except Exception:
            raise Exception("Not found")

    return clientstat

def create_clientstatus(data):
    new_clientstatus = ClientStatus(descripcion=data['descripcion'])
    new_clientstatus.save()
    return new_clientstatus

def update_clientstatus(clientstat):
    client_updated = ClientStatus.objects.get(id=clientstat['id'])
    client_updated.descripcion=clientstat['descripcion']
    client_updated.active=clientstat['active']
    client_updated.save()
    return client_updated

#Prioridad
def get_prioridad_by_id(id):
    if not id:
        raise Exception('id not provided.')
    try:
        prior = Prioridad.objects.get(id=id)
    except Exception:
        raise Exception("Not found")
    return prior

def get_prioridades(active):
    if(active):
        try:
            prior = Prioridad.objects.filter(active=active)
        except Exception:
            raise Exception("Not found")
    else:
        try:
            prior = Prioridad.objects.filter()
        except Exception:
            raise Exception("Not found")

    return prior

def create_prioridad(data):
    new_prior = Prioridad(descripcion=data['descripcion'])
    new_prior.save()
    return new_prior

def update_prioridad(prioridad):
    prior = Prioridad.objects.get(id=prioridad['id'])
    prior.descripcion=prioridad['descripcion']
    prior.active=prioridad['active']
    prior.save()
    return prior

#MediosDePago
def get_mediodepago_by_id(id):
    if not id:
        raise Exception('id not provided.')
    try:
        mediodepago = MedioDePago.objects.get(id=id)
    except Exception:
        raise Exception("Not found")
    return mediodepago

def get_mediosdepago(active):
    if(active):
        try:
            mediodepago = MedioDePago.objects.filter(active=active)
        except Exception:
            raise Exception("Not found")
    else:
        try:
            mediodepago = MedioDePago.objects.filter()
        except Exception:
            raise Exception("Not found")

    return mediodepago

def create_mediodepago(data):
    mediodepago = MedioDePago(descripcion=data['descripcion'])
    mediodepago.save()
    return mediodepago

def update_mediodepago(mediodepago):
    mdepago = MedioDePago.objects.get(id=mediodepago['id'])
    mdepago.descripcion=mediodepago['descripcion']
    mdepago.active=mediodepago['active']
    mdepago.save()
    return mdepago

    
#Users
def create_user(data):
    new_usr = User(
        email=data['email'],
        password=data['password'],
        name=data['name'],
        rut=data['rut'],
        role=data['role'],
        age=18)

    user_settings = UserSettings(id=new_usr.id,
                                 theme='default')
    new_usr.save()
    user_settings.save()
    return new_usr

def get_user_by_id(id):
    if not id:
        raise Exception('id not provided.')
    try:
        user = User.objects.get(id=id)
    except Exception:
        raise Exception("Not found")
    return user

def get_users(active):
    if(active):
        try:
            users = User.objects.filter(active=active)
        except Exception:
            raise Exception("Not found")
    else:
        try:
            users = User.objects.filter()
        except Exception:
            raise Exception("Not found")

    return users

def update_user(user):
    usr = User.objects.get(email=user['email'])
    usr.name=user['name']
    usr.rut=user['rut']
    usr.active=user['active']
    usr.role=user['role']
    usr.password=user['password']
    usr.save()
    return usr 

def generate_password_hash(password):
    return handler.hash(secret=password)


#TechOrder
def get_techorder_by_ordertype_id(id):
    if not id:
        raise Exception('id not provided.')
    try:
        techorders = Technician.objects.filter(type_orders__id=id)
    except Exception:
        techorders = ''
    return techorders

def get_techorder_by_tech_rut(rut):
    if not rut:
        raise Exception('rut not provided.')
    try:
        techorders = Technician.objects.filter(rut=rut)
    except Exception:
        techorders = ''
    return techorders

def create_techordertype(request):
    if not request['tecnico_rut']:
        raise Exception('tecnico_rut not provided')
    try:
        techorders = Technician.objects.get(rut=request['tecnico_rut'])
    except Exception:
        raise Exception("Not found")
    
    if not request['ordertype_id']:
        raise Exception('ordertype_id not provided')
    try:
        order = OrderType.objects.get(id=request['ordertype_id'])
    except Exception:
        raise Exception("Not found")

    techorders.type_orders.add(order)
    return techorders

def delete_techordertype(request):
    try:
        request['tecnico_rut']
    except:
        raise Exception('tecnico_rut not provided')

    try:
        techorders = Technician.objects.get(rut=request['tecnico_rut'])
    except Exception:
        raise Exception("Not found")
    
    if not request['ordertype_id']:
        raise Exception('ordertype_id not provided')
    try:
        order = OrderType.objects.get(id=request['ordertype_id'])
    except Exception:
        raise Exception("Not found")

    techorders.type_orders.remove(order)
    return techorders


#UserAssignedTech
def get_user_assigned_tech_by_user_email(email):
    if not email:
        raise Exception('email not provided.')
    try:
        techorders = Technician.objects.filter(assigned_user__email=email)
    except Exception:
        techorders = ''
    return techorders

def get_user_assigned_tech_by_tech_rut(rut):
    if not rut:
        raise Exception('rut not provided.')
    try:
        techorders = Technician.objects.filter(rut=rut)
    except Exception:
        techorders = ''
    return techorders

def create_user_assigned_tech(request):
    if not request['tecnico_rut']:
        raise Exception('tecnico_rut not provided')
    try:
        techorders = Technician.objects.get(rut=request['tecnico_rut'])
    except Exception:
        raise Exception("Not found")
    
    if not request['user_email']:
        raise Exception('user_email not provided')
    try:
        user = User.objects.get(email=request['user_email'])
    except Exception:
        raise Exception("Not found")

    techorders.assigned_user.add(user)
    return techorders

def delete_user_assigned_tech(request):
    try:
        request['tecnico_rut']
    except:
        raise Exception('tecnico_rut not provided')

    try:
        techorders = Technician.objects.get(rut=request['tecnico_rut'])
    except Exception:
        raise Exception("Not found")
    
    if not request['user_email']:
        raise Exception('user_email not provided')
    try:
        user = User.objects.get(email=request['user_email'])
    except Exception:
        raise Exception("Not found")

    techorders.assigned_user.remove(user)
    return techorders

def get_orderchecker(rut):
    valid = 0
    order = ''
    try:
        client = get_client_by_rut(rut)
        
        if(client):
            date_init = datetime.date.today()
            date_end = (datetime.date.today() + timedelta(days=14))
            order = Order.objects.filter(client_order__rut__contains=client.rut,fechaejecucion__range=[date_init,date_end],estadoticket__id__in=[1,2,3,5,6])
            if(order):
                valid = 0
            else:
                valid = 1
        else:
            valid= -2
    except:
        valid = -3

    return valid