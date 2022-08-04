
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from .models import Drone, Medication, Transportation

class DroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = '__all__'
        
class MedicationSerializer(serializers.ModelSerializer):    
    image = Base64ImageField(required=False)
    class Meta:
        model = Medication
        fields = ('name', 'weight','code', 'image')
                
class TransportationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transportation
        fields = '__all__'