from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from therapymeeting.settings import TWILIO_ACCOUNT_SID,TWILIO_ACCOUNT_TOKEN
from .models import  MeetingDetails, ParentsMeeting , messageLog
import phonenumbers
from phonenumbers import PhoneNumberFormat
from twilio.rest import Client

def sendMassage(whatsNum):
    try:
        with transaction.atomic():
            # client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)
            # get_last_url=MeetingDetails.objects.values_list('meeting_URL', flat=True).last()
            # if get_last_url:
            #     send_message = client.messages.create(
            #     from_='whatsapp:+14155238886',
            #     body=get_last_url,
            #     to=f'whatsapp:{whatsNum}'
            #     )
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)
            message = client.messages.create(
            content_sid="HX351c8a839e87a544ad9068de4ce3d33d",
            from_='whatsapp:+201026267878',
            to=f'whatsapp:{whatsNum}'
            )

            contxt={
                "SID": message.sid,
                "Status": message.status,
                "From": message.from_,
                "To": message.to,
                "Body": message.body,
                "Date Sent": message.date_sent,
                "Error Code": message.error_code,
                "Error Message": message.error_message
            }
            messageLog.objects.create(To=whatsNum , Log= str(contxt))
    except Exception as error:
        messageLog.objects.create(To=whatsNum , Log= str(error))

def index(request):
    if request.method == 'POST':
        with transaction.atomic():
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
                    
                    sendMassage(phone_number)
                    messages.success(request, "Form Submitted Successfully.")
                    render(request, 'index.html')
                else:
                    messages.error(request, "Invalid phone number for the given country code.")
            except phonenumbers.NumberParseException:
                messages.error(request, "Invalid phone number format.")
            except Exception as error:
                messages.error(request, "You Can't Submmit More than once Per Week ")
    

    return render(request, 'index.html')