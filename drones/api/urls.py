from django.urls import path

from .views import *

urlpatterns = [
    #always id is drone id
    path('drones/', DronesList.as_view(), name='drones_list'),
    path('drones/<int:id>/', DroneOperations.as_view(), name='drones_operations' ),
    path('drones_availables/', DronesAvailables.as_view(), name='drones_availables'),
    path('drone_battery/<int:id>/', DroneBatteryStatus.as_view(), name='drone_battery' ),
    path('drone_medications/<int:id>/', DroneMedications.as_view(), name='drone_medications'),
    path('drone_state/<int:id>/', drone_change_state, name='drone_state'),
    
    
    path('drones_battery_logs/', DroneBatteryLogList.as_view(), name='drones_battery_logs_list'),
    path('drones_battery_logs/<int:id>/', DroneBatteryOperations.as_view(), name='drones_battery_logs_opertions'),
    
    # id is medication id
    path('medications/', MedicationsList.as_view(), name='medications_list'),
    path('medications/<int:id>/', MedicationOperations.as_view(), name='medications_operations'),
    
    # id is transportation id
    path('transportations/', TransportationList.as_view(), name='transportations_list'),
    path('transportations/<int:id>/', TransportationOperations.as_view(), name='transportations_operations'),
]