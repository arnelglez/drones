from django.shortcuts import render, get_object_or_404

from django.utils.translation import  gettext_lazy as _

# rest-framework api imports
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse

# function to obtain model name by model index
def drone_model_load(index):
    if index == 0:
        result = 'Lightweight'
    elif index == 1:
        result ='Middleweight'
    elif index == 2:
        result = 'Cruiserweight'
    return result

# function to obtain max weight by model
def drone_weight_capacity(data):
    model = int(data['model'])
    weight = float(data['weight'])
    errors = []
    #    model 0 max weight = 200          model 1 max weight = 300        model 2 max weight = 400
    if (model == 0 and weight > 200) or (model == 1 and weight > 300) or (model == 2 and weight > 400):
        errors.append(_("For model {} max weight is {}".format(drone_model_load(model), str((int(model)*100)+200) + 'g')))
    return data, errors

class MixinsList:
    model = None
    classSerializer = None
    
    def get(self, request):
        # Search all objects of model
        obj = self.model.objects.all()
        # serializes all object
        serializers = self.classSerializer(obj, many=True)
        # Show list of object
        return JsonResponse(serializers.data, safe=False, status=status.HTTP_200_OK)
    
    def post(self, request):
        # verify class is Drone
        if self.model.__name__.lower() == 'drone':
            #verify that the weight matches the model, only for drones
            data, errors = self.drone_weight_capacity(request.data)
            # if there are errors return them
            if errors.__len__() > 0:
                return JsonResponse(errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = request.data
        # serializes data entry
        objSerializer = self.classSerializer(data=data)
        # verify if entry is valid
        if objSerializer.is_valid(): 
            # save entry               
            objSerializer.save()
            # show object saved 
            return JsonResponse(objSerializer.data, safe=False, status=status.HTTP_201_CREATED)
        # show errors because not save  
        return JsonResponse(objSerializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
    

class MixinOperations:
    model = None
    classSerializer = None
    
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