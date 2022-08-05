
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from .models import Drone, Medication, Transportation, TransportationMedication

class DroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = ('id', 'serial', 'model', 'weight', 'battery', 'state')
        
class DroneBatterySerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = ('id', 'battery')
        
class MedicationSerializer(serializers.ModelSerializer):    
    image = Base64ImageField(required=False)
    class Meta:
        model = Medication
        fields = ('name', 'code', 'weight', 'image')


class TransportationMedicationSerializer(serializers.ModelSerializer):
    medication_name = serializers.ReadOnlyField(source="medication.name")    
    class Meta:
        model = TransportationMedication
        fields = ('id', 'transportation', 'medication', 'medication_name', 'amount')     
        extra_kwargs = {
            'transportation' : {
                'write_only' : True,
            } 
        }

class DroneMedicationSerializer(serializers.ModelSerializer):
    medication_name = serializers.ReadOnlyField(source="medication.name")    
    class Meta:
        model = TransportationMedication
        fields = ('id', 'transportation', 'medication', 'medication_name', 'amount')    

class TransportationSerializer(serializers.ModelSerializer):
    medications = TransportationMedicationSerializer(many=True, read_only=True ,source="transportationmedication_set")
    class Meta:
        model = Transportation
        fields = ('id', 'drone', 'status' ,'medications')
