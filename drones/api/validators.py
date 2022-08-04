
import re
from django.core.exceptions import ValidationError
from django.utils.translation import  gettext_lazy as _


def serial_drone(value):
    if not value.isdigit():
        raise ValidationError(_('Serial has be a number'))
    return value
        
def weight_drone(value):
    if value > 500:
        raise ValidationError(_('Max weght is 500 g'))
    return value
    
def batery_drone(value):
    if value < 0:
        raise ValidationError(_('Batery charge cant be lower than 0'))
    if value > 100:
        raise ValidationError(_('Batery charge cant be upper than 100'))
    return value

def name_medication(value):
    if  re.search(r'[^a-zA-Z0-9_/-]', value):
        raise ValidationError(_('Name allow only letters, numbers, underscore and middlescore'))
    return value

def code_medication(value):
    if  re.search(r'[^A-Z0-9_]', value):
        raise ValidationError(_('Code allow only uppercase letters, numbers and underscore'))
    return value
