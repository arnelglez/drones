from django.shortcuts import render, get_object_or_404

# rest-framework api imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class MixinsList:
    model = None
    classSerializer = None
    
    def get(self, request):
        # Search all objects of model
        obj = self.model.objects.all()
        # serializes all object
        serializers = self.classSerializer(obj, many=True)
        # Show list of object
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        # serializes data entry
        objSerializer = self.classSerializer(data=request.data)
        # verify if entry is valid
        if objSerializer.is_valid(): 
            # save entry               
            objSerializer.save()
            # show object saved 
            return Response(objSerializer.data, status=status.HTTP_201_CREATED)
        # show errors because not save  
        return Response(objSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MixinOperations:
    model = None
    classSerializer = None
    
    def get(self, request, id):
        # Search object by id
        obj = get_object_or_404(self.model, id__iexact = id)
        # serializes object
        serializer = self.classSerializer(obj, many=False)
        # show object
        return Response(serializer.data, status=status.HTTP_200_OK)
        
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
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        # show errors because not save 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        # Search object by id
        obj = get_object_or_404(self.model, id__iexact = id)   
        # delete entry                 
        obj.delete()    
        # show blank object (deleted)   
        return Response(status=status.HTTP_204_NO_CONTENT)