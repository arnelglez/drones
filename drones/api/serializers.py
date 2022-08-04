
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from django.utils.translation import  gettext_lazy as _


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
            # this function validate load max weight, battery level for drone use and if drone be disponible
    
        def create(self, validated_data):
            weight = 0
            drone = Drone.objects.filter(id=object.validated_data.get('drone')).first()
            medications = object.validated_data.get('medications')
            for medication in medications:
                weight += Medication.objects.filter(id = medication).first().weight
            # if medicamentations weight more than drone can load raise error
            if drone.weight < weight:
                raise serializers.ValidationError(_("This drone can't be load this weight, is max load is {}g".format(drone.weight)))
            #if drone battery level is down 25% then raise error
            if drone.battery <= 25:
                raise serializers.ValidationError(_("This drone can't be load with this battery level, minimum is 25{} and has {}".format('%', drone.weight+'%')))
            # if drone don't be IDLE raise error
            if drone.state != 0:
                raise serializers.ValidationError(_("This drone is in use"))
        # else return object
            return validated_data