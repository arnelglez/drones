import json

from django.urls import reverse
from rest_framework import  status
from rest_framework.test import APITestCase

from .models import Drone, Medication, Transportation, TransportationMedication

class DroneViewTestCase(APITestCase):
    
    def drones_setUp(self):
        self.drone = Drone.objects.create( serial = "1234567890",
                                          model = "1", 
                                          weight = "400",
                                          battery = "80", 
                                          state = "0"
                                        )
       
    def test_list_drones(self):
        response = self.client.get(reverse('drones_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def edit_drone(self):
        self.drone = Drone.objects.create( serial = "1234567890",
                                          model = "3", 
                                          weight = "300",
                                          battery = "80", 
                                          state = "0"            
                                        )
        response = self.client.put(reverse('drones_operations pk=1'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)