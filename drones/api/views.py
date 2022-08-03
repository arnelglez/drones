from email.mime import image
from django.shortcuts import render, get_object_or_404

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
    model = Transportation
    classSerializer = TransportationSerializer
    