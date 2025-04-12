from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from therapymeeting.settings import TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN
from .models import MeetingDetails, ParentsMeeting, messageLog
import phonenumbers
from phonenumbers import PhoneNumberFormat
from twilio.rest import Client

import time
from twilio.base.exceptions import TwilioRestException
from django.db import transaction


def sendMassage(whatsNum):
    try:
        with transaction.atomic():
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)
            message = client.messages.create(
                content_sid="HX3fd9ae5de3443d8b3151a54aa7fa4795",
                from_="whatsapp:+201007477581",
                to=f"whatsapp:{whatsNum}",
            )

            # Polling until the message status is 'sent', 'delivered', or 'failed'
            while True:
                time.sleep(1)  # Wait for 2 seconds before checking the status
                message_status = client.messages(message.sid).fetch().status
                if message_status.lower() in [
                    "delivered",
                    "failed",
                    "undelivered",
                    "read",
                ]:
                    break

            # Collecting message details
            message_details = client.messages(message.sid).fetch()
            contxt = {
                "SID": message_details.sid,
                "Status": message_details.status,
                "From": message_details.from_,
                "To": message_details.to,
                "Body": message_details.body,
                "Date Sent": message_details.date_sent,
                "Error Code": message_details.error_code,
                "Error Message": message_details.error_message,
            }
            messageLog.objects.create(
                To=whatsNum,
                Log=contxt,
                SID=message_details.sid,
                Status=message_details.status,
                Error_Code=message_details.error_code,
                Error_Message=message_details.error_message,
            )

            return message_status

    except TwilioRestException as error:
        messageLog.objects.create(
            To=whatsNum,
            Log=str(error),
            SID=message_details.sid,
            Status=message_details.status,
            Error_Code=message_details.error_code,
            Error_Message=message_details.error_message,
        )
        return "failed"
    except Exception as e:
        messageLog.objects.create(
            To=whatsNum,
            Log=str(e),
            SID=message_details.sid,
            Status=message_details.status,
            Error_Code=message_details.error_code,
            Error_Message=message_details.error_message,
        )
        return "failed"


def sendAlertMassage(whatsNum):
    try:
        with transaction.atomic():
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)
            message = client.messages.create(
                content_sid="HXa70d3cd6b0b260c1810c8cc4c07ede33",
                from_="whatsapp:+201007477581",
                to=f"whatsapp:{whatsNum}",
            )

            # Polling until the message status is 'sent', 'delivered', or 'failed'
            while True:
                time.sleep(1)  # Wait for 2 seconds before checking the status
                message_status = client.messages(message.sid).fetch().status
                if message_status.lower() in [
                    "delivered",
                    "failed",
                    "undelivered",
                    "read",
                ]:
                    break

            # Collecting message details
            message_details = client.messages(message.sid).fetch()
            contxt = {
                "SID": message_details.sid,
                "Status": message_details.status,
                "From": message_details.from_,
                "To": message_details.to,
                "Body": message_details.body,
                "Date Sent": message_details.date_sent,
                "Error Code": message_details.error_code,
                "Error Message": message_details.error_message,
            }
            messageLog.objects.create(
                To=whatsNum,
                Log=contxt,
                SID=message_details.sid,
                Status=message_details.status,
                Error_Code=message_details.error_code,
                Error_Message=message_details.error_message,
            )

            return message_status

    except TwilioRestException as error:
        messageLog.objects.create(
            To=whatsNum,
            Log=str(error),
            SID=message_details.sid,
            Status=message_details.status,
            Error_Code=message_details.error_code,
            Error_Message=message_details.error_message,
        )

        return f"Error: {error}"
    except Exception as e:
        messageLog.objects.create(
            To=whatsNum,
            Log=str(e),
            SID=message_details.sid,
            Status=message_details.status,
            Error_Code=message_details.error_code,
            Error_Message=message_details.error_message,
        )
        return "failed"


def sendFacebookGroup(whatsNum):
    try:
        with transaction.atomic():
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)
            message = client.messages.create(
                content_sid="HXa70d3cd6b0b260c1810c8cc4c07ede33",
                from_="whatsapp:+201007477581",
                to=f"whatsapp:{whatsNum}",
            )

            # Polling until the message status is 'sent', 'delivered', or 'failed'
            while True:
                time.sleep(1)  # Wait for 2 seconds before checking the status
                message_status = client.messages(message.sid).fetch().status
                if message_status.lower() in [
                    "delivered",
                    "failed",
                    "undelivered",
                    "read",
                ]:
                    break

            # Collecting message details
            message_details = client.messages(message.sid).fetch()
            contxt = {
                "SID": message_details.sid,
                "Status": message_details.status,
                "From": message_details.from_,
                "To": message_details.to,
                "Body": message_details.body,
                "Date Sent": message_details.date_sent,
                "Error Code": message_details.error_code,
                "Error Message": message_details.error_message,
            }
            messageLog.objects.create(
                To=whatsNum,
                Log=contxt,
                SID=message_details.sid,
                Status=message_details.status,
                Error_Code=message_details.error_code,
                Error_Message=message_details.error_message,
            )

            return message_status

    except TwilioRestException as error:
        messageLog.objects.create(
            To=whatsNum,
            Log=str(error),
            SID=message_details.sid,
            Status=message_details.status,
            Error_Code=message_details.error_code,
            Error_Message=message_details.error_message,
        )

        return f"Error: {error}"
    except Exception as e:
        messageLog.objects.create(
            To=whatsNum,
            Log=str(e),
            SID=message_details.sid,
            Status=message_details.status,
            Error_Code=message_details.error_code,
            Error_Message=message_details.error_message,
        )
        return "failed"


def index(request):
    if request.method == "POST":
        try:
            with transaction.atomic():
                # Get form data
                full_name = request.POST.get("full_name")
                phone_number = request.POST.get("phone_number")
                country_code = request.POST.get("country_code", "US")
                email = request.POST.get("email")
                # Validate the phone number
                try:
                    parsed_number = phonenumbers.parse(phone_number, country_code)
                    if phonenumbers.is_valid_number(parsed_number):
                        formatted_phone_number = phonenumbers.format_number(
                            parsed_number, PhoneNumberFormat.E164
                        )

                        # Save the form data to the database
                        form_obj = ParentsMeeting.objects.create(
                            full_name=full_name,
                            phone_number=formatted_phone_number,
                            country_code=country_code,
                            email=email,
                        )

                        # Send the message and check status
                        status = sendMassage(formatted_phone_number)

                        if status == "failed":
                            raise Exception("Message sending failed, please try again.")

                        # If the message was successfully sent
                        messages.success(
                            request,
                            "Form Submitted Successfully, kindly check your whatsapp",
                        )
                        return render(request, "index.html")

                    else:
                        messages.error(
                            request, "Invalid phone number for the given country code."
                        )
                except phonenumbers.NumberParseException:
                    messages.error(
                        request, "Invalid phone number format, please try again."
                    )

        except Exception as error:
            messages.error(request, str(error))

    return render(request, "index.html")




# 🌟 تأكيد حضور ورشة "كيف تتعامل مع المدمن حتى يقتنع بالعلاج" 🌟

# مرحبًا!

# نشكر لكم تواصلكم معنا سابقًا ويسعدنا تأكيد تسجيلكم في ورشتنا القادمة بعنوان "كيف تتعامل مع المدمن حتى يقتنع بالعلاج"، التي ستقام يوم السبت المقبل بمشاركة الأستاذ سعد المحمود وفريق من المعالجين النفسيين والأخصائيين.

# 📍 المكان: عبر جوجل ميت. يمكنكم الانضمام عبر الرابط التالي: https://meet.google.com/czq-wicr-vva

# 🕒 الوقت: الساعة الخامسة مساءً بتوقيت السعودية.

# 💬 لأي استفسار أو تواصل إضافي، يمكنكم مراسلتنا عبر الرقم: +962 7 9838 5260



# 🌟 تأكيد حضور ورشة "كيف تتعامل مع المدمن حتى يقتنع بالعلاج" 🌟

# ملاحظة هامة:
# خلال شهر رمضان المبارك، سيصبح موعد الورشة يوم الجمعة الساعة ٢ ظهرًا بتوقيت السعودية.

# مرحبًا!
# نشكر لكم تواصلكم معنا، ويسعدنا تأكيد تسجيلكم في الورشة القادمة بمشاركة الأستاذ سعد المحمود وفريق من الخبراء.

# 📅 الموعد الجديد:
# الجمعة المقبلة
# ⏰ ٢ ظهرًا (توقيت السعودية)

# 📍 طريقة الحضور:
# عبر منصة Google Meet
# انضمام مباشر من هنا:
# https://meet.google.com/czq-wicr-vva

# 📞 للتواصل:
# +962 7 9838 5260
