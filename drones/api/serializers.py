
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from .models import Drone, Medication, Transportation, TransportationMedication

class DroneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drone
        fields = '__all__'
        
class MedicationSerializer(serializers.ModelSerializer):    
    image = Base64ImageField(required=False)
    class Meta:
        model = Medication
        fields = ('name', 'weight','code', 'image')


class TransportationMedicationSerializer(serializers.ModelSerializer):
    medication_name = serializers.ReadOnlyField(source="medication.name")    
    class Meta:
        model = TransportationMedication
        fields = ('id', 'transportation', 'medication', 'amount', 'medication_name')     

class TransportationSerializer(serializers.ModelSerializer):
    medications = TransportationMedicationSerializer(many=True, read_only=True ,source="transportationmedication_set")
    class Meta:
        model = Transportation
        fields = '__all__'
