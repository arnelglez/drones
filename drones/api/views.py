from email.mime import image
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from django.utils.translation import  gettext_lazy as _

# rest-framework api imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Drone, Medication, Transportation
from .serializers import DroneSerializer, MedicationSerializer, TransportationSerializer
from .utils import MixinOperations, MixinsList, MixinOperations, drone_weight_capacity

# Create your views here.

class DronesList(MixinsList, APIView):    
    model = Drone
    classSerializer = DroneSerializer
    
    def post(self, request):
        #verify that the weight matches the model
        data, errors = drone_weight_capacity(request.data)
        # if there are errors return them
        if errors.__len__() == 0:        
            # serializes data entry
            objSerializer = DroneSerializer(data=data)
            # verify if entry is valid
            if objSerializer.is_valid(): 
                # save entry               
                objSerializer.save()
                # show object saved 
                return JsonResponse(objSerializer.data, safe=False, status=status.HTTP_201_CREATED)
            # show errors because not save  
            return JsonResponse(objSerializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
    
class DroneOperations(APIView):    
    def get(self, request, id):
        # Search object by id
        obj = get_object_or_404(self.model, id__iexact = id)
        # serializes object
        serializer = self.classSerializer(obj, many=False)
        # show object
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        
    def put(self, request, id):
        # Search object by id
        obj = get_object_or_404(self.model, id__iexact = id)
        
        # serializes data entry
        serializer = self.classSerializer(obj, data=request.data)
        # verify if entry is valid
        if(serializer.is_valid()):
            # save entry               
            serializer.save()     
            # show object updated    
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_202_ACCEPTED)
        # show errors because not save 
        return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        # Search object by id
        obj = get_object_or_404(self.model, id__iexact = id)   
        # delete entry                 
        obj.delete()    
        # show blank object (deleted)   
        return JsonResponse(safe=False, status=status.HTTP_204_NO_CONTENT)
    
class MedicationsList(MixinsList, APIView):
    model = Medication
    classSerializer = MedicationSerializer
    
class MedicationOperations(MixinOperations, APIView):
    model = Medication
    classSerializer = MedicationSerializer
    
class TransportationList(MixinsList, APIView):
    def get(self, request):
        # Search all objects of model
        obj = Transportation.objects.all()
        # serializes all object
        serializers = TransportationSerializer(obj, many=True)
        # Show list of object   
        return JsonResponse(serializers.data, safe=False, status=status.HTTP_200_OK)
    
    # this function validate load max weight, battery level for drone use and if drone be disponible
    def weigth_load(self, data):
        totalWeight = 0
        errors = []
        drone = get_object_or_404(Drone, id=data['drone'])
        medications = data['medications']
        for med in medications:
            medication = get_object_or_404(Medication, id = med)
            weight = medication.weight
            amount = medication.amount
            totalWeight += weight * amount
            # if medicamentations weight more than drone can load raise error
        if drone.weight <= totalWeight:
            errors.append(_("This drone can't be load this weight, is max load is {}g".format(str(drone.weight))))
        #if drone battery level is down 25% then raise error
        if drone.battery <= 25:
            errors.append(_("This drone can't be load with this battery level, minimum is 25{} and has {}".format('%', str(drone.battery)+'%')))
        # if drone don't be IDLE raise error
        if drone.state != 0:
            errors.append(_("This drone is in use"))
        # else return object
        
        return data, errors, drone
    
    def post(self, request):
        # verify state, wegth and battery
        data, errors, drone = self.weigth_load(request.data)
        # verifies don't has errors
        if errors.__len__() == 0 :
            # serializes data entry
            objSerializer = TransportationSerializer(data=data)
            # verify if entry is valid
            if objSerializer.is_valid():  
                pass           
                # save entry               
                objSerializer.save()
                # change drone state to loading
                drone.state = 1
                # save drone state
                drone.save()
                # show object saved 
                return JsonResponse(objSerializer.data, safe=False, status=status.HTTP_201_CREATED)
            
            # show errors because not save  
            return JsonResponse(objSerializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
    