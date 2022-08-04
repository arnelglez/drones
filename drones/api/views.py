from email.mime import image
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from django.core.exceptions import ValidationError
from django.utils.translation import  gettext_lazy as _

# rest-framework api imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Drone, Medication, Transportation
from .serializers import DroneSerializer, MedicationSerializer, TransportationSerializer
from .utils import MixinOperations, MixinsList, MixinOperations

# Create your views here.

class DronesList(MixinsList, APIView):
    model = Drone
    classSerializer = DroneSerializer
    
class DroneOperations(MixinOperations ,APIView):
    model = Drone
    classSerializer = DroneSerializer
    
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
    

    
    def post(self, request):
        # serializes data entry
        objSerializer = TransportationSerializer(data=request.data)
        # verify if entry is valid
        if objSerializer.is_valid():             
            # save entry               
            objSerializer.save()
            drone = get_object_or_404(Drone ,objSerializer.data['drone'])
            drone.state = 1
            drone.save()
            # show object saved 
            return JsonResponse(objSerializer.data, safe=False, status=status.HTTP_201_CREATED)
        
        # show errors because not save  
        return JsonResponse(objSerializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
    