from rest_framework import serializers
from ..models import Residence

class ResidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Residence
        fields = ['id', 'comuna', 'direccion', 'mac', 'pppoe', 'client']