
from pkg_resources import require
from rest_framework import serializers
from .models import Drone, Medication, Transportation

class DroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = '__all__'
        
class MedicationSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Medication
        fields = '__all__'
                
class TransportationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transportation
        fields = '__all__'