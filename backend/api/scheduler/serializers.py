from rest_framework import serializers
from ..models import Residence,Order

class ResidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Residence
        fields = ['id', 'comuna', 'direccion', 'mac', 'pppoe', 'client']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Residence
        fields = ['id', 'tipo', 'prioridad', 'disponibilidad', 'comentario', 'fechaejecucion','estadocliente','estadoticket','mediodepago','monto','created_at','created_by','encargado','client_order','client_residence']