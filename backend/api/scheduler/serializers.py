from rest_framework import serializers
from ..models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','role','password','name','rut','active']
        #fields = '__all__'

class OrderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderType
        fields = '__all__'

class TrackingSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Tracking
        fields = '__all__'

class ClientStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientStatus
        fields = '__all__'

class TicketStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketStatus
        fields = '__all__'

class PrioridadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prioridad
        fields = '__all__'

class MedioDePagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prioridad
        fields = '__all__'

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
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    encargado = TechnicianSerializer(read_only=True)
    client_order = ClientSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    client_residence = ResidenceSerializer(read_only=True)
    tipo = OrderTypeSerializer(read_only=True)
    estadocliente = ClientStatusSerializer(read_only=True)
    estadoticket = TicketStatusSerializer(read_only=True)
    mediodepago = MedioDePagoSerializer(read_only=True)
    prioridad = PrioridadSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

'''
class TrackingSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Tracking
        fields = '__all__'
'''