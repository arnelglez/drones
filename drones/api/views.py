from email.mime import image
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from django.utils.translation import  gettext_lazy as _

# rest-framework api imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Drone, Medication, Transportation, TransportationMedication
from .serializers import DroneSerializer, MedicationSerializer, TransportationSerializer, TransportationMedicationSerializer
from .utils import MixinOperations, MixinsList, MixinOperations, drone_weight_capacity

# Create your views here.

class DronesList(MixinsList, APIView):    
    model = Drone
    classSerializer = DroneSerializer
    
    # overwrites function post of MixinsList in utils.py
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
    
class DroneOperations(MixinOperations ,APIView):      
    model = Drone
    classSerializer = DroneSerializer    
    
    # overwrites function put of MixinOperations in utils.py    
    def put(self, request, id):
        # Search object by id
        #verify that the weight matches the model
        data, errors = drone_weight_capacity(request.data)
        # if there are errors return them
        if errors.__len__() == 0:   
            drone = get_object_or_404(Drone, id__iexact = id)
            #search active transportation
            trasnsportation = Transportation.objects.filter(drone=drone.id).filter(status=1).first()
            
            # serializes data entry
            serializer = DroneSerializer(drone, data=data)
            # verify if entry is valid
            if(serializer.is_valid()):
                # save entry               
                serializer.save()    
                # verifi transportation exist and drone state is 0 
                if trasnsportation and serializer.state == 0:
                    # transportation inactive
                    trasnsportation.status = 0
                    # save trasnsportation
                    trasnsportation.save()
                # show object updated    
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_202_ACCEPTED)
            # show errors because not save 
            return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
    
    # overwrites function delete of MixinOperations in utils.py  
    def delete(self, request, id):
        # Search object by id
        drone = get_object_or_404(Drone, id__iexact = id)   
        # if drone is not in use delete entry                 
        if drone.state == 0:
            drone.delete()   
            # show blank object (deleted)   
            return JsonResponse( {},safe=False, status=status.HTTP_204_NO_CONTENT)
        else: 
            # show blank object (deleted)   
            return JsonResponse(_("Can't delete drone if is in use") ,safe=False, status=status.HTTP_401_UNAUTHORIZED)
            
    
class MedicationsList(MixinsList, APIView):
    model = Medication
    classSerializer = MedicationSerializer
    
class MedicationOperations(MixinOperations, APIView):
    model = Medication
    classSerializer = MedicationSerializer
    
class TransportationList(MixinsList, APIView):
    model = Transportation
    classSerializer = TransportationSerializer
    
    # this function validate load max weight, battery level for drone use and if drone be disponible
    def weigth_load(self, data):
        totalWeight = 0
        errors = []
        drone = get_object_or_404(Drone, id=data['drone'])
        medications = data['medications']
        for med in medications:
            medication = get_object_or_404(Medication, id = med['medication'])
            weight = medication.weight
            amount = med['amount']
            totalWeight += weight * amount
            # if medicamentations weight more than drone can load raise error
        if drone.weight <= totalWeight:
            errors.append(_("This drone can't be load this weight {}g, is max load is {}g".format(str(totalWeight) ,str(drone.weight))))
        #if drone battery level is down 25% then raise error
        if drone.battery <= 25:
            errors.append(_("This drone can't be load with this battery level, minimum is 25{} and has {}".format('%', str(drone.battery)+'%')))
        # if drone don't be IDLE raise error
        if drone.state != 0:
            errors.append(_("This drone is in use"))
        # else return object
        
        return data, errors, medications ,drone
    
    def post(self, request):
        # verify state, wegth and battery
        data, errors, transMedList, drone = self.weigth_load(request.data)
        # verifies don't has errors
        if errors.__len__() == 0 :     
            # serializes data entry
            transportationSerializer = TransportationSerializer(data=data)
            # verify if entry is valid
            if transportationSerializer.is_valid():              
                # save entry  
                transportationSerializer.save()
                
                # change drone state to loading
                drone.state = 1
                # save drone state
                drone.save()
                
                # run transmed entraces to create json with this datas to save
                for transMed in transMedList:                
                    trans = transportationSerializer.data['id']                   
                    medic = transMed['medication']
                    amount = transMed['amount']
                    
                    # create json
                    createTransMed = {
                        "transportation" : trans,                    
                        "medication" : medic,
                        "amount" : amount,
                        } 
                    
                    # serialize create json
                    createTransMedSerializer = TransportationMedicationSerializer(data=createTransMed)
                    if createTransMedSerializer.is_valid():
                        # save data
                        createTransMedSerializer.save()
                # show object saved 
                return JsonResponse(transportationSerializer.data, safe=False, status=status.HTTP_201_CREATED)
                
            # show errors because not save  
            return JsonResponse(transportationSerializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(errors, safe=False, status=status.HTTP_400_BAD_REQUEST)

class TransportationOperations(MixinOperations, APIView):
    model = Transportation
    classSerializer = TransportationSerializer
    
    # overwrites function put of MixinOperations in utils.py   
    def put(self, request, id):
        # Search object by id
        obj = get_object_or_404(Transportation, id__iexact = id)
        
        # serializes data entry
        serializer = TransportationSerializer(obj, data=request.data)
        # verify if entry is valid
        if(serializer.is_valid()):
            # save entry               
            serializer.save()     
            # show object updated    
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_202_ACCEPTED)
        # show errors because not save 
        return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
    
    # overwrites function delete of MixinOperations in utils.py   
    def delete(self, request, id):
        # Search object by id
        obj = get_object_or_404(Transportation, id__iexact = id)   
        # delete entry                 
        obj.delete()    
        # show blank object (deleted)   
        return JsonResponse({},safe=False, status=status.HTTP_204_NO_CONTENT)