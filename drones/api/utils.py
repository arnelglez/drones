from django.shortcuts import render, get_object_or_404

# rest-framework api imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class MixinsList:
    model = None
    classSerializer = None
    
    def get(self, request):
        obj = self.model.objects.all()
        serializers = self.classSerializer(obj, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        objSerializer = self.classSerializer(data=request.data)
        
        if objSerializer.is_valid():                
            objSerializer.save()
            return Response(objSerializer.data, status=status.HTTP_201_CREATED)
         
        return Response(objSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MixinObjects:
    model = None
    classSerializer = None
    
    def get(self, request, id):
        obj = get_object_or_404(self.model, id__iexact = id)
        serializer = self.classSerializer(obj, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def put(self, request, id):
        obj = get_object_or_404(self.model, id__iexact = id)
        
        serializer = self.classSerializer(obj, data=request.data)

        if(serializer.is_valid()):
            serializer.save()        
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        obj = get_object_or_404(self.model, id__iexact = id)        
        obj.delete()       
        return Response(status=status.HTTP_204_NO_CONTENT)