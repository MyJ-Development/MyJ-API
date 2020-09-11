from django.db import models
from django.conf import settings
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser

class User(AbstractBaseUser, PermissionsMixin):
    id = models.IntegerField(unique=True, primary_key=True)
    email = models.CharField(max_length=30) 
    password = models.CharField(max_length=100)
    first_name = models.CharField(default='', max_length=15)
    last_name = models.CharField(default='', max_length=15)
    login = models.CharField(max_length=15)
    age = models.IntegerField()
    street = models.CharField(blank=True, max_length=255)
    city = models.CharField(blank=True, max_length=255)
    zip = models.CharField(blank=True, max_length=10)
    role = models.CharField(default='', max_length=10)

    USERNAME_FIELD = 'id'


class UserSettings(models.Model):
    id = models.OneToOneField(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              primary_key=True)
    theme = models.CharField(max_length=10)

class Client(models.Model):
    rut = models.CharField(max_length=11,primary_key=True)
    nombre = models.CharField(max_length=50)
    email = models.CharField(blank=True,max_length=50)
    contacto1 = models.CharField(max_length=13)
    contacto2 = models.CharField(blank=True,max_length=13)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True)
    created_by = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='client2createdby')
    updated_by = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name='client2updatedby')


class Residence(models.Model):
    id = models.AutoField(primary_key=True)
    comuna = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    mac = models.CharField(blank=True,max_length=12)
    pppoe = models.CharField(blank=True,max_length=50)
    client = models.ForeignKey(Client,on_delete=models.DO_NOTHING)

class Technician(models.Model):
    id = models.IntegerField(primary_key=True)
    rut = models.CharField(max_length=11,blank=True)
    comuna = models.CharField(blank=True, max_length=50)
    nombre = models.CharField(max_length=50)
    estado = models.CharField(blank=True,max_length=50)
    capacidad = models.IntegerField(blank=True)

cliente_estados = (
    ("No aplicable","no aplicable"),
    ("Confirmado","confirmado"),
    ("Sin Factibilidad","sin factibilidad"),
    ("Deuda cliente","deuda cliente"),
    ("Deuda domicilio","deuda domicilio"),
    ("Responsabilidad cliente","responsabilidad cliente"),
    ("Sin contacto","sin contacto"),
    ("Confirmado cuenta creada","confirmado cuenta creada")
)

ticket_estados = (
    ("No aplicable","no aplicable"),
    ("En proceso","en proceso"),
    ("Tecnico no acude","tecnico no acude"),
    ("Cerrado","cerrado"),
    ("Cerrado no terminado","cerrado no terminado")
)

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=50)
    prioridad = models.CharField(max_length=50)
    disponibilidad = models.CharField(blank=True,max_length=50)
    comentario = models.CharField(max_length=300,blank=True)
    fechaejecucion = models.DateTimeField(blank=False)
    estadocliente = models.CharField(max_length=30,choices=cliente_estados,default="No aplicable")
    estadoticket =  models.CharField(max_length=30,choices=ticket_estados,default="No aplicable")
    mediodepago = models.CharField(max_length=30,blank=True)
    monto = models.IntegerField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,blank=True,on_delete=models.DO_NOTHING)
    encargado = models.ForeignKey(Technician,blank=True,on_delete=models.DO_NOTHING)
    client_order = models.ForeignKey(Client,blank=True,on_delete=models.DO_NOTHING)

class Tracking(models.Model):
    id = models.AutoField(primary_key=True)
    comentario = models.CharField(max_length=300)
    created_by = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='tracking2created')
    created_at = models.DateTimeField(auto_now_add=True)



