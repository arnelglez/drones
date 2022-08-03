
from pkg_resources import require
from rest_framework_json_api import serializers
from .models import Drone, Medication, Transportation

class DroneSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Drone
        fields = '__all__'
        
class MedicationSerializer(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = Medication
        fields = '__all__'
        
        
class TransportationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transportation
        fields = '__all__'