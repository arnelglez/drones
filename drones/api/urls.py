from django.urls import path

from .views import *

urlpatterns = [
    path('drones/', DronesList.as_view(), name='drone_list' ),
    path('drones/<int:id>/', DroneOperations.as_view(), name='drone_operations' ),
    
    path('medications/', MedicationsList.as_view(), name='medication_list' ),
    path('transportation/', TransportationList.as_view(), name='transportation_list' ),
    
]