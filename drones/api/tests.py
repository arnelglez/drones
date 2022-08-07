import json

from django.urls import reverse
from rest_framework import  status
from rest_framework.test import APITestCase

from .models import Drone, DroneBatteryLog ,Medication, Transportation, TransportationMedication

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
    
    def test_details_drone(self):
        '''
        Ensure we can show any drone details.
        '''
        url = '/api/drones/1/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Drone.objects.first().serial, "1234567890")
    
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
        self.assertEqual(Drone.objects.count(), 3)  
       
    def test_list_drones_availables(self):
        '''
        Ensure we can list all drones.
        '''
        response = self.client.get(reverse('drones_availables'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertEqual(response.json()[0]['id'], 1)
       
    def test_list_drone_battery(self):
        '''
        Ensure we can check drone battery level for a given drone.
        '''
        url = '/api/drone_battery/2/'      
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)   
        self.assertEqual(response.json()['battery'], 60)
        
    def test_drone_change_state(self):
        '''
        Ensure we can change drone state for a given drone.
        '''
        url = '/api/drone_state/2/'    
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)   
        self.assertEqual(response.json()['state'], 3)
        
        
        

class DroneBatteryLogTestCase(APITestCase):
    '''
    Class testing Drones
    '''
    def setUp(self):
        '''
        Init data in drones db
        '''
        drone1 = Drone.objects.create(serial = "1234567890", model = "0", weight = "199", battery = "70", state = "0")
        drone2 = Drone.objects.create(serial = "1234567891", model = "1", weight = "285", battery = "60", state = "2")
        drone3 = Drone.objects.create(serial = "1234567892", model = "2", weight = "393", battery = "50", state = "3")
        drone4 = Drone.objects.create(serial = "1234567893", model = "3", weight = "470", battery = "30", state = "5")   
        
        DroneBatteryLog.objects.create(drone=drone1, battery=50) 
        DroneBatteryLog.objects.create(drone=drone1, battery=40) 
        DroneBatteryLog.objects.create(drone=drone1, battery=60)         
        DroneBatteryLog.objects.create(drone=drone2, battery=60) 
        DroneBatteryLog.objects.create(drone=drone3, battery=60) 
        DroneBatteryLog.objects.create(drone=drone4, battery=60) 
    
    def test_create_log_fail(self):
        '''
        Ensure we can't create a new drone object.
        '''
        url = reverse('drones_battery_logs_list')
        data = {"drone" : "1", "battery" : "70"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
       
    def test_list_drones_logs(self):
        '''
        Ensure we can list all drones logs.
        '''
        response = self.client.get(reverse('drones_battery_logs_list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DroneBatteryLog.objects.count(), 6)    
    
    def test_details_drone_logs(self):
        '''
        Ensure we can show any drone logs details.
        '''
        url = '/api/drones_battery_logs/1/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DroneBatteryLog.objects.filter(drone=1).count(), 3)
        
    def test_edit_drone_log_fail(self):
        '''
        Ensure we can't edited any drone.
        '''
        url = '/api/drones_battery_logs/1/'
        data = {"drone" : "1", "battery" : "70"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_delete_drone_log_fail(self):
        '''
        Ensure we can't delete any drone
        '''
        url = '/api/drones_battery_logs/1/'      
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)   
           

class MedicationTestCase(APITestCase):
    '''
    Class testing Medications
    '''
    myImage = "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" 
       
    def setUp(self):
        '''
        Init data in medications db
        ''' 
        Medication.objects.create(name = "medications", weight = "15", code = "AA_55555_AA", image = self.myImage)
        Medication.objects.create(name = "medications1", weight = "17", code = "AA_55555_AB", image = self.myImage)
        Medication.objects.create(name = "medications2", weight = "20", code = "AA_55555_AC", image = self.myImage)
        Medication.objects.create(name = "medications3", weight = "18", code = "AA_55555_AD", image = self.myImage)
    
    
    def test_create_medication(self):
        '''
        Ensure we can create a new medication object.
        '''
        url = reverse('medications_list')
        data = {"name" : "medications4", "weight" : "10", "code" : "FF_55555_DD", "image" : self.myImage}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Medication.objects.count(), 5)
       
    def test_list_medications(self):
        '''
        Ensure we can list all medications.
        '''
        response = self.client.get(reverse('medications_list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Medication.objects.count(), 4)
    
    def test_details_medication(self):
        '''
        Ensure we can show any medication details.
        '''
        url = '/api/medications/1/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Medication.objects.first().code, "AA_55555_AA")       
    
    def test_edit_medication(self):
        '''
        Ensure we can edited any medication.
        '''
        url = '/api/medications/1/'
        data = {"name" : "medications4", "weight" : "10", "code" : "FF_55555_DD", "image" : self.myImage}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Medication.objects.count(), 4)
        
    def test_delete_medication(self):
        '''
        Ensure we can delete any medication
        '''
        url = '/api/medications/3/'        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Medication.objects.count(), 3)
        

class TransportationTestCase(APITestCase):
    '''
    Class testing Transportations
    '''
    def setUp(self):
        '''
        Init data in transportations db
        '''        
        drone1 = Drone.objects.create(serial = "1234567890", model = "0", weight = "199", battery = "70", state = "0")
        drone2 = Drone.objects.create(serial = "1234567891", model = "1", weight = "285", battery = "60", state = "2")
        drone3 = Drone.objects.create(serial = "1234567892", model = "2", weight = "393", battery = "50", state = "3")
        drone4 = Drone.objects.create(serial = "1234567893", model = "3", weight = "470", battery = "30", state = "5")  
        drone5 = Drone.objects.create(serial = "1234567894", model = "3", weight = "470", battery = "90", state = "0")  
        
        med1 = Medication.objects.create(name = "medications", weight = "15", code = "AA_55555_AA", image = "myImage.jpg")
        med2 = Medication.objects.create(name = "medications1", weight = "17", code = "AA_55555_AB", image = "myImage.jpg")
        med3 = Medication.objects.create(name = "medications2", weight = "20", code = "AA_55555_AC", image = "myImage.jpg")
        med4 = Medication.objects.create(name = "medications3", weight = "18", code = "AA_55555_AD", image = "myImage.jpg")
        
        trans1 = Transportation.objects.create(drone = drone4, status="1")   
        trans2 = Transportation.objects.create(drone = drone2, status="1")   
        trans3 = Transportation.objects.create(drone = drone3, status="1")   
        trans4 = Transportation.objects.create(drone = drone1, status="1")   
                
        TransportationMedication.objects.create(transportation = trans1, medication = med1, amount = "3")
        TransportationMedication.objects.create(transportation = trans1, medication = med2, amount = "5")
        TransportationMedication.objects.create(transportation = trans2, medication = med3, amount = "3") 
        TransportationMedication.objects.create(transportation = trans3, medication = med3, amount = "2")
        TransportationMedication.objects.create(transportation = trans3, medication = med4, amount = "1")
        TransportationMedication.objects.create(transportation = trans3, medication = med1, amount = "3")
        TransportationMedication.objects.create(transportation = trans4, medication = med2, amount = "3")
        TransportationMedication.objects.create(transportation = trans4, medication = med3, amount = "4")
            
    def test_create_transportation(self):
        '''
        Ensure we can create a new transportation object.
        '''
        url = reverse('transportations_list')
        data = {
                "drone" : 5,
                "medications" : [
                    { "medication": 2, "amount": 3 },
                    { "medication": 1, "amount": 2 },
                    ],
                "status" : 1
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transportation.objects.count(), 5)
               
       
    def test_list_transportations(self):
        '''
        Ensure we can list all transportations.
        '''
        response = self.client.get(reverse('transportations_list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Transportation.objects.count(), 4)
    
    def test_details_transportations(self):
        '''
        Ensure we can show any transportation details.
        '''
        url = '/api/transportations/1/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Transportation.objects.first().drone.serial, "1234567893")               
    
    def test_edit_transportation(self):
        '''
        Ensure we can edited any transportation.
        '''
        url = '/api/transportations/1/'
        data = {
                "drone" : 1,
                "medications" : [
                    { "medication": 2, "amount": 3 },
                    { "medication": 1, "amount": 2 },
                    ],
                "status" : 1
                }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Transportation.objects.count(), 4)
        
    def test_delete_transportation(self):
        '''
        Ensure we can delete any transportation
        '''
        url = '/api/transportations/2/'        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Transportation.objects.count(), 3)
        

    def test_drone_medication_list(self):
        '''
        Ensure we can check loaded medication items for a given dronee.
        '''
        url = '/api/drone_medications/3/'     
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)   