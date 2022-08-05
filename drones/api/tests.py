import json

from django.urls import reverse
from rest_framework import  status
from rest_framework.test import APITestCase

from .models import Drone, Medication, Transportation, TransportationMedication

class DroneTestCase(APITestCase):
    '''
    Class testing Drones
    '''
    def setUp(self):
        '''
        Init data in drones db
        '''
        Drone.objects.create(serial = "1234567890", model = "0", weight = "199", battery = "70", state = "0")
        Drone.objects.create(serial = "1234567891", model = "1", weight = "285", battery = "60", state = "2")
        Drone.objects.create(serial = "1234567892", model = "2", weight = "393", battery = "50", state = "3")
        Drone.objects.create(serial = "1234567893", model = "3", weight = "470", battery = "30", state = "5")    
    
    def test_create_drone(self):
        '''
        Ensure we can create a new drone object.
        '''
        url = reverse('drones_list')
        data = {"serial" : "1234567895", "model" : "3", "weight" : "200", "battery" : "70", "state" : "1"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Drone.objects.count(), 5)               
       
    def test_list_drones(self):
        '''
        Ensure we can list all drones.
        '''
        response = self.client.get(reverse('drones_list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Drone.objects.count(), 4)        
    
    def test_edit_drone(self):
        '''
        Ensure we can edited any drone.
        '''
        url = '/api/drones/1/'
        data = {"serial" : "1234567898", "model" : "2", "weight" : "400", "battery" : "25", "state" : "5"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Drone.objects.count(), 4)
        
    def test_delete_drone(self):
        '''
        Ensure we can delete any drone
        '''
        url = '/api/drones/1/'        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, 3)  
       
    def test_list_drones_availables(self):
        '''
        Ensure we can list all drones.
        '''
        response = self.client.get(reverse('drones_availables'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Drone.objects.filter(state=0).first(), 1)
    '''
    
    'drone_battery/2/'
    'drone_medications/3/
    
    '''
class MedicationTestCase(APITestCase):
    '''
    Class testing Medications
    '''
    def setUp(self):
        '''
        Init data in medications db
        '''
      #(allowed only upper case letters, underscore and numbers);
    
        Medication.objects.create(name = "AA_bb-1111", weight = "15", code = "AA_55555_AA", image = "meicine1.jpg")
        Medication.objects.create(name = "AA_bb-1111", weight = "17", code = "AA_55555_AB", image = "meicine2.jpg")
        Medication.objects.create(name = "AA_bb-1111", weight = "20", code = "AA_55555_AC", image = "meicine3.jpg")
        Medication.objects.create(name = "AA_bb-1111", weight = "18", code = "AA_55555_AD", image = "meicine4.jpg")
    
    
    def test_create_medication(self):
        '''
        Ensure we can create a new medication object.
        '''
        '''url = reverse('medications_list')
        data = {"serial" : "1234567895", "model" : "3", "weight" : "200", "battery" : "70", "state" : "1"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Medication.objects.count(), 5)'''
               
       
    def test_list_medications(self):
        '''
        Ensure we can list all medications.
        '''
        '''response = self.client.get(reverse('medications_list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Medication.objects.count(), 4)'''
        
    
    def test_edit_medication(self):
        '''
        Ensure we can edited any medication.
        '''
        '''url = '/api/medications/1/'
        data = {"serial" : "1234567898", "model" : "2", "weight" : "400", "battery" : "25", "state" : "5"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Medication.objects.count(), 4)'''
        
    def test_delete_medication(self):
        '''
        Ensure we can delete any medication
        '''
        '''url = '/api/medications/1/'        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Medication.objects.count(), 3)'''
        
    