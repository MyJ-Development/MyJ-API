from rest_framework import serializers
from ..models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','role']

class OrderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderType
        fields = ['id','descripcion']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        created_by = UserSerializer(read_only=True)
        fields = '__all__'

class ResidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Residence
        client = ClientSerializer(read_only=True)
        fields = '__all__'

class TechnicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technician
        fields = ['id', 'rut', 'comuna', 'nombre', 'estado', 'capacidad']

class OrderSerializer(serializers.ModelSerializer):
    encargado = TechnicianSerializer(read_only=True)
    client_order = ClientSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    client_residence = ResidenceSerializer(read_only=True)
    tipo = OrderTypeSerializer(read_only=True)
    class Meta:
        model = Order
        fields = '__all__'

