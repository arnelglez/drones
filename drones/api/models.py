from tokenize import blank_re
from django.db import models
from django.urls import reverse

from .validators import *

class Drone(models.Model):
    CHOISES_MODEL = (
        (0 , 'Lightweight'), #weight up to 200g
        (1 , 'Middleweight'), #weight up to 300g
        (2 , 'Cruiserweight'), #weight up to 400g
        (3 , 'Heavyweight') #weight up to 500g
    )
    
    CHOISES_STATE = (
        (0 , 'IDLE'),
        (1 , 'LOADING'),
        (2 , 'LOADED'),
        (3 , 'DELIVERING'),
        (4 , 'DELIVERED'),
        (5 , 'RETURNING')
    )
    serial = models.CharField(max_length=100, validators=[serial_drone], unique=True) #number (100 characters max)
    model = models.IntegerField(choices=CHOISES_MODEL, default = 0) #(Lightweight, Middleweight, Cruiserweight, Heavyweight)
    weight = models.FloatField(max_length=5, validators=[weight_drone]) # limit (500gr max)
    battery = models.FloatField(validators=[batery_drone]); #capacity (percentage)
    state = models.IntegerField(choices=CHOISES_STATE, default = 0) #(IDLE, LOADING, LOADED, DELIVERING, DELIVERED, RETURNING)
    
    def __str__(self):
        return self.serial
    
class Medication(models.Model):    
    name = models.CharField(max_length=150, validators=[name_medication]) #allowed only letters, numbers, ‘-‘, ‘_’);
    weight = models.FloatField()
    code = models.CharField(max_length=150, validators=[code_medication]) #(allowed only upper case letters, underscore and numbers);
    image = models.ImageField(null=True, upload_to='medication/', blank=True) #(picture of the medication case).
    
    
    def __str__(self):
        return self.name
    
class Transportation(models.Model):
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
    medications = models.ManyToManyField(Medication, related_name='medications')
    amount = models.IntegerField()
    
    def __str__(self):
        return self.drone