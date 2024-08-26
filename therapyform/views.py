from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import  ParentsMeeting
import phonenumbers
from phonenumbers import PhoneNumberFormat

def index(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        country_code = request.POST.get('country_code', 'US')
        email =request.POST.get('email')
        # Validate the phone number
        try:
            parsed_number = phonenumbers.parse(phone_number, country_code)
            if phonenumbers.is_valid_number(parsed_number):
                formatted_phone_number = phonenumbers.format_number(parsed_number, PhoneNumberFormat.E164)
                form_obj = ParentsMeeting.objects.create(full_name=full_name, phone_number=formatted_phone_number
                                          ,country_code=country_code
                                          ,email=email)
                
                messages.success(request, "Form Submitted Successfully.")
                render(request, 'index.html')
            else:
                messages.error(request, "Invalid phone number for the given country code.")
        except phonenumbers.NumberParseException:
            messages.error(request, "Invalid phone number format.")
    
    return render(request, 'index.html')