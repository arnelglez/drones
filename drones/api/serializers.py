
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from .models import Drone, Medication, Transportation, TransportationMedication

class DroneSerializer(serializers.ModelSerializer):
    '''
    class Drone serializer
    '''
    class Meta:
        model = Drone
        fields = ('id', 'serial', 'model', 'weight', 'battery', 'state')
        
class DroneBatterySerializer(serializers.ModelSerializer):
    '''
    class Drone serializer only for show battery status by id
    '''
    class Meta:
        model = Drone
        fields = ('id', 'battery')
        
class MedicationSerializer(serializers.ModelSerializer):  
    '''
    class Medication serializer
    '''  
    image = Base64ImageField(required=False)
    class Meta:
        model = Medication
        fields = ('name', 'code', 'weight', 'image')


class TransportationMedicationSerializer(serializers.ModelSerializer):
    '''
    class TransportationMedication
    '''
    # field include to show medication name
    medication_name = serializers.ReadOnlyField(source="medication.name")    
    class Meta:
        model = TransportationMedication
        fields = ('id', 'transportation', 'medication', 'medication_name', 'amount')    
        # include because transportation field is only to save, don't show 
        extra_kwargs = {
            'transportation' : {
                'write_only' : True,
            } 
        }

class DroneMedicationSerializer(serializers.ModelSerializer):
    '''
    class DroneMedication serializer only for show medicamentations load by drone
    '''
    # field include to show medication name
    medication_name = serializers.ReadOnlyField(source="medication.name")    
    class Meta:
        model = TransportationMedication
        fields = ('id', 'transportation', 'medication', 'medication_name', 'amount')    

class TransportationSerializer(serializers.ModelSerializer):
    '''
    class Transportation
    '''
    # field include to use meny to many relationship
    medications = TransportationMedicationSerializer(many=True, read_only=True ,source="transportationmedication_set")
    class Meta:
        model = Transportation
        fields = ('id', 'drone', 'status' ,'medications')
