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
        return Response(serializers.data)
    
    def post(self, request):
        objSerializer = self.classSerializer(data=request.data)
        
        if objSerializer.is_valid():                
            objSerializer.save()
            return Response(objSerializer.data, status=status.HTTP_201_CREATED)
        
        return Response(objSerializer.errors, status=status.HTTP_400_BAD_REQUEST)