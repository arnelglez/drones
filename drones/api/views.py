from email.mime import image
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from django.utils.translation import  gettext_lazy as _

# rest-framework api imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Drone, Medication, Transportation, TransportationMedication
from .serializers import DroneSerializer, DroneBatterySerializer, DroneMedicationSerializer ,MedicationSerializer, TransportationSerializer, TransportationMedicationSerializer
from .utils import MixinOperations, MixinsList, MixinOperations, drone_weight_capacity


def weigth_load(data, id = None):
    '''
    this function validate load max weight, battery level for drone use and if drone be disponible
    '''
    totalWeight = 0
    errors = []
    drone = get_object_or_404(Drone, id=data['drone'])
    medications = data['medications']
    # verify alls medicamentation to optain total weigth
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
    if drone.state != 0 and id == None:
        errors.append(_("This drone is in use"))
    # else return object
    
    return data, errors, medications ,drone

def save_transportation_medication(transMedList, trans):
    '''
        Save TransportationsMedications Objects
    '''
    # run transmed entraces to create json with this datas to save
    for transMed in transMedList:                                
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
            
            
# Create your views here.

class DronesList(MixinsList, APIView):    
    model = Drone
    classSerializer = DroneSerializer
    
    
    def post(self, request):
        '''
        overwrites function post of MixinsList in utils.py
        '''
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
    
   
    def put(self, request, id):
        '''
        overwrites function put of MixinOperations in utils.py 
        '''
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
                if trasnsportation and serializer.data['state'] == 0:
                    # transportation inactive
                    trasnsportation.status = 0
                    # save trasnsportation
                    trasnsportation.save()
                # show object updated    
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_202_ACCEPTED)
            # show errors because not save 
            return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
    
     
    def delete(self, request, id):
        '''
        overwrites function delete of MixinOperations in utils.py 
        '''
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

class DronesAvailables(APIView):
    def get(self, request):
        '''
         check available drones for loading
        '''
        # Search availables objects of model
        drones = Drone.objects.filter(state = 0)
        # serializes all object
        serializers = DroneSerializer(drones, many=True)
        # Show list of object
        return JsonResponse(serializers.data, safe=False, status=status.HTTP_200_OK)            
    
class DroneBatteryStatus(APIView):
    '''
    check drone battery level for a given drone
    '''
    def get(self, request, id):
        # Search availables objects of model
        drone = get_object_or_404(Drone, id=id)
        # serializes all object
        serializers = DroneBatterySerializer(drone, many=False)
        # Show list of object
        return JsonResponse(serializers.data, safe=False, status=status.HTTP_200_OK)    

class DroneMedications(APIView):
    def get(self, request, id):
        '''
        checking loaded medication items for a given drone
        '''
        # Search availables objects of model
        drone = get_object_or_404(Drone, id=id)
        # Search transportation active for this drone
        transportation = Transportation.objects.filter(drone=drone.id).filter(status=True).first()
        transMed = TransportationMedication.objects.filter(transportation = transportation)
        # serializes all object
        serializers = DroneMedicationSerializer(transMed, many=True)
        # Show list of object
        return JsonResponse(serializers.data, safe=False, status=status.HTTP_200_OK)  




class MedicationsList(MixinsList, APIView):
    model = Medication
    classSerializer = MedicationSerializer
    
class MedicationOperations(MixinOperations, APIView):
    model = Medication
    classSerializer = MedicationSerializer
    
class TransportationList(MixinsList, APIView):
    model = Transportation
    classSerializer = TransportationSerializer
    
    def post(self, request):
        '''
        overwrites function post of MixinsList in utils.py 
        '''
        # verify state, wegth and battery
        data, errors, transMedList, drone = weigth_load(request.data)
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
                
                # load transportation id
                trans = transportationSerializer.data['id']   
                save_transportation_medication(transMedList, trans)
                # show object saved 
                transportation = get_object_or_404(Transportation, id=trans)
                transportationSerializer = TransportationSerializer(transportation)
                return JsonResponse(transportationSerializer.data, safe=False, status=status.HTTP_201_CREATED)
                
            # show errors because not save  
            return JsonResponse(transportationSerializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(errors, safe=False, status=status.HTTP_400_BAD_REQUEST)

class TransportationOperations(MixinOperations, APIView):
    model = Transportation
    classSerializer = TransportationSerializer
       
    def put(self, request, id):
        '''
        overwrites function put of MixinOperations in utils.py
        '''
        # Search object by id
        transportation = get_object_or_404(Transportation, id__iexact = id)
        data, errors, transMedList, drone = weigth_load(request.data, id)
        # verifies don't has errors
        if errors.__len__() == 0 :   
            
            # serializes data entry
            serializer = TransportationSerializer(transportation, data=data)
            # verify if entry is valid
            if(serializer.is_valid()):
                # verify: transportation do not begined
                if drone.state > 2:
                    # show error: transportations in process cannot be edited
                    return JsonResponse(_('Transportations in process cannot be edited'), safe=False, status=status.HTTP_400_BAD_REQUEST)
                else: 
                    # save entry               
                    serializer.save()     
                    
                    # load transportation id
                    trans = serializer.data['id']   
                    # load all medications loaded in this transportation
                    transportationMedications = TransportationMedication.objects.filter(transportation = trans)
                    # delete every medications in this transportation
                    for transMed in transportationMedications:
                        transMed.delete() 
                        
                    save_transportation_medication(transMedList, trans)
                    # show object saved 
                    transportation = get_object_or_404(Transportation, id=trans)
                    serializer = TransportationSerializer(transportation)
                    
                    # show object updated    
                    return JsonResponse(serializer.data, safe=False, status=status.HTTP_202_ACCEPTED)
                # show errors because not save 
            return JsonResponse(serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
      
    def delete(self, request, id):
        '''
        overwrites function delete of MixinOperations in utils.py 
        '''
        # Search object by id
        transportation = get_object_or_404(Transportation, id__iexact = id)  
        # search drone for verify transportation state
        drone = get_object_or_404(Drone, id=transportation.drone.id)
        # verify: transportation do not begined
        if drone.state > 2:
            # show error: transportations in process cannot be deleted
            return JsonResponse(_('Transportations in process cannot be deleted'), safe=False, status=status.HTTP_400_BAD_REQUEST)
        else:     
            # delete entry              
            transportation.delete()    
            # show blank object (deleted)   
            return JsonResponse({},safe=False, status=status.HTTP_204_NO_CONTENT)


        