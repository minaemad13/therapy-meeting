from django.db import models
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class ParentsMeeting  (models.Model):
    full_name =models.CharField(max_length=100,null=False,blank=False ,default='From File')
    email = models.EmailField(max_length=100,null=False,blank=False ,default='default@default.com')
    phone_number = PhoneNumberField(region="JO")  # Default region
    country_code=models.CharField(max_length=10,null=False,blank=False,default='JO')
    creation_Date = models.DateField(auto_now_add=True)
    # class Meta:
    #     unique_together = ('email', 'phone_number','creation_Date')
        
    def __str__(self) -> str:
        return self.full_name + ' - ' + self.email 


class MeetingDetails (models.Model):
    Title =models.CharField(max_length=100,null=False,blank=False)
    meeting_date = models.DateTimeField(null=False,blank=False)
    meeting_URL = models.URLField(null=False,blank=False)
    creation_Date = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.Title + ' - ' + str(self.meeting_date )

class messageLog (models.Model):
    To =models.CharField(max_length=30,null=False,blank=False)
    Log = models.CharField(max_length=1000,null=False,blank=False)
    SID=models.CharField(max_length=80,null=False,blank=False)
    Status= models.CharField(max_length=100,null=False,blank=False)
    Error_Code= models.CharField(max_length=100,null=True,blank=True,default='0')
    Error_Message= models.CharField(max_length=100,null=True,blank=True,default='Success')
    creation_Date = models.DateField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.To + ' - ' + str(self.creation_Date )
