from django.db import models
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class ParentsMeeting  (models.Model):
    full_name =models.CharField(max_length=100,null=False,blank=False)
    email = models.EmailField(max_length=100,null=False,blank=False)
    phone_number = PhoneNumberField(region="US")  # Default region
    country_code=models.CharField(max_length=10,null=False,blank=False)
    creation_Date = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.full_name + ' - ' + self.email 
    