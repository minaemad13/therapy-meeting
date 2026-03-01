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
from django.http import JsonResponse
import json
import datetime
import requests
import time
from twilio.base.exceptions import TwilioRestException
from django.db import transaction
import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


def sendMassage(whatsNum):
    try:
        # FIXED: Removed transaction.atomic() to prevent database locks on long API calls
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)
        message = client.messages.create(
            content_sid="HXc085bd122cee48f9b59d00a4d9b395d8",
            from_="whatsapp:+201007477581",
            to=f"whatsapp:{whatsNum}",
        )

        # FIXED: Added a max attempts break to prevent an infinite background loop
        attempts = 0
        while attempts < 15:
            time.sleep(1)
            message_status = client.messages(message.sid).fetch().status
            if message_status.lower() in ["delivered", "failed", "undelivered", "read"]:
                break
            attempts += 1

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
        # FIXED: Replaced message_details.sid with None since it doesn't exist on failure
        messageLog.objects.create(
            To=whatsNum,
            Log=str(error),
            SID=None, 
            Status="failed",
            Error_Code=error.code,
            Error_Message=error.msg,
        )
        return "failed"
    except Exception as e:
        messageLog.objects.create(
            To=whatsNum,
            Log=str(e),
            SID=None,
            Status="failed",
            Error_Code=None,
            Error_Message=str(e),
        )
        return "failed"


def sendAlertMassage(whatsNum):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)
        message = client.messages.create(
            content_sid="HX450859cbb03c9de8588dac4d610bf835",
            from_="whatsapp:+201007477581",
            to=f"whatsapp:{whatsNum}",
        )

        attempts = 0
        while attempts < 15:
            time.sleep(1)
            message_status = client.messages(message.sid).fetch().status
            if message_status.lower() in ["delivered", "failed", "undelivered", "read"]:
                break
            attempts += 1

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
            SID=None,
            Status="failed",
            Error_Code=error.code,
            Error_Message=error.msg,
        )
        return f"Error: {error}"
    except Exception as e:
        messageLog.objects.create(
            To=whatsNum,
            Log=str(e),
            SID=None,
            Status="failed",
            Error_Code=None,
            Error_Message=str(e),
        )
        return "failed"


def sendRamadanMsgGroup(whatsNum):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)
        message = client.messages.create(
            content_sid="HX58291911eaef8744ed88447e9833d8d4",
            from_="whatsapp:+201007477581",
            to=f"whatsapp:{whatsNum}",
        )

        attempts = 0
        while attempts < 15:
            time.sleep(1)
            message_status = client.messages(message.sid).fetch().status
            if message_status.lower() in ["delivered", "failed", "undelivered", "read"]:
                break
            attempts += 1

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
            SID=None,
            Status="failed",
            Error_Code=error.code,
            Error_Message=error.msg,
        )
        return f"Error: {error}"
    except Exception as e:
        messageLog.objects.create(
            To=whatsNum,
            Log=str(e),
            SID=None,
            Status="failed",
            Error_Code=None,
            Error_Message=str(e),
        )
        return "failed"

# def sendMassage(whatsNum):
#     try:
#         with transaction.atomic():
#             client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)
#             message = client.messages.create(
#                 content_sid="HXc085bd122cee48f9b59d00a4d9b395d8",
#                 from_="whatsapp:+201007477581",
#                 to=f"whatsapp:{whatsNum}",
#             )

#             # Polling until the message status is 'sent', 'delivered', or 'failed'
#             while True:
#                 time.sleep(1)  # Wait for 2 seconds before checking the status
#                 message_status = client.messages(message.sid).fetch().status
#                 if message_status.lower() in [
#                     "delivered",
#                     "failed",
#                     "undelivered",
#                     "read",
#                 ]:
#                     break

#             # Collecting message details
#             message_details = client.messages(message.sid).fetch()
#             contxt = {
#                 "SID": message_details.sid,
#                 "Status": message_details.status,
#                 "From": message_details.from_,
#                 "To": message_details.to,
#                 "Body": message_details.body,
#                 "Date Sent": message_details.date_sent,
#                 "Error Code": message_details.error_code,
#                 "Error Message": message_details.error_message,
#             }
#             messageLog.objects.create(
#                 To=whatsNum,
#                 Log=contxt,
#                 SID=message_details.sid,
#                 Status=message_details.status,
#                 Error_Code=message_details.error_code,
#                 Error_Message=message_details.error_message,
#             )

#             return message_status

#     except TwilioRestException as error:
#         messageLog.objects.create(
#             To=whatsNum,
#             Log=str(error),
#             SID=message_details.sid,
#             Status=message_details.status,
#             Error_Code=message_details.error_code,
#             Error_Message=message_details.error_message,
#         )
#         return "failed"
#     except Exception as e:
#         messageLog.objects.create(
#             To=whatsNum,
#             Log=str(e),
#             SID=message_details.sid,
#             Status=message_details.status,
#             Error_Code=message_details.error_code,
#             Error_Message=message_details.error_message,
#         )
#         return "failed"


# def sendAlertMassage(whatsNum):
#     try:
#         with transaction.atomic():
#             client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)
#             message = client.messages.create(
#                 content_sid="HX450859cbb03c9de8588dac4d610bf835",
#                 from_="whatsapp:+201007477581",
#                 to=f"whatsapp:{whatsNum}",
#             )

#             # Polling until the message status is 'sent', 'delivered', or 'failed'
#             while True:
#                 time.sleep(1)  # Wait for 2 seconds before checking the status
#                 message_status = client.messages(message.sid).fetch().status
#                 if message_status.lower() in [
#                     "delivered",
#                     "failed",
#                     "undelivered",
#                     "read",
#                 ]:
#                     break

#             # Collecting message details
#             message_details = client.messages(message.sid).fetch()
#             contxt = {
#                 "SID": message_details.sid,
#                 "Status": message_details.status,
#                 "From": message_details.from_,
#                 "To": message_details.to,
#                 "Body": message_details.body,
#                 "Date Sent": message_details.date_sent,
#                 "Error Code": message_details.error_code,
#                 "Error Message": message_details.error_message,
#             }
#             messageLog.objects.create(
#                 To=whatsNum,
#                 Log=contxt,
#                 SID=message_details.sid,
#                 Status=message_details.status,
#                 Error_Code=message_details.error_code,
#                 Error_Message=message_details.error_message,
#             )

#             return message_status

#     except TwilioRestException as error:
#         messageLog.objects.create(
#             To=whatsNum,
#             Log=str(error),
#             SID=message_details.sid,
#             Status=message_details.status,
#             Error_Code=message_details.error_code,
#             Error_Message=message_details.error_message,
#         )

#         return f"Error: {error}"
#     except Exception as e:
#         messageLog.objects.create(
#             To=whatsNum,
#             Log=str(e),
#             SID=message_details.sid,
#             Status=message_details.status,
#             Error_Code=message_details.error_code,
#             Error_Message=message_details.error_message,
#         )
#         return "failed"


# def sendRamadanMsgGroup(whatsNum):
#     try:
#         with transaction.atomic():
#             client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)
#             message = client.messages.create(
#                 content_sid="HXb30e05fa9973841cbcca623be539d04c",
#                 from_="whatsapp:+201007477581",
#                 to=f"whatsapp:{whatsNum}",
#             )

#             # Polling until the message status is 'sent', 'delivered', or 'failed'
#             while True:
#                 time.sleep(1)  # Wait for 2 seconds before checking the status
#                 message_status = client.messages(message.sid).fetch().status
#                 if message_status.lower() in [
#                     "delivered",
#                     "failed",
#                     "undelivered",
#                     "read",
#                 ]:
#                     break

#             # Collecting message details
#             message_details = client.messages(message.sid).fetch()
#             contxt = {
#                 "SID": message_details.sid,
#                 "Status": message_details.status,
#                 "From": message_details.from_,
#                 "To": message_details.to,
#                 "Body": message_details.body,
#                 "Date Sent": message_details.date_sent,
#                 "Error Code": message_details.error_code,
#                 "Error Message": message_details.error_message,
#             }
#             messageLog.objects.create(
#                 To=whatsNum,
#                 Log=contxt,
#                 SID=message_details.sid,
#                 Status=message_details.status,
#                 Error_Code=message_details.error_code,
#                 Error_Message=message_details.error_message,
#             )

#             return message_status

#     except TwilioRestException as error:
#         messageLog.objects.create(
#             To=whatsNum,
#             Log=str(error),
#             SID=message_details.sid,
#             Status=message_details.status,
#             Error_Code=message_details.error_code,
#             Error_Message=message_details.error_message,
#         )

#         return f"Error: {error}"
#     except Exception as e:
#         messageLog.objects.create(
#             To=whatsNum,
#             Log=str(e),
#             SID=message_details.sid,
#             Status=message_details.status,
#             Error_Code=message_details.error_code,
#             Error_Message=message_details.error_message,
#         )
#         return "failed"


from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

def sendSmsAlphanumeric(phoneNum, message_body, sender_id="Restart"):
    # تعريف المتغيرات مبدئياً لتفادي خطأ (UnboundLocalError) في حال فشل الإرسال من البداية
    msg_sid = "Failed-No-SID" # بدلاً من None
    msg_status = "failed"
    msg_error_code = 0 # أو أي رقم افتراضي يقبله حقل الأرقام لديك
    msg_error_message = "Failed before contacting Twilio"
    
    phoneNum = str(phoneNum)
    try:
        with transaction.atomic():
            # تهيئة الاتصال (تأكد من تعريف TWILIO_ACCOUNT_SID و TWILIO_AUTH_TOKEN في ملفك)
            client = Client(TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN)
            # 1. إنشاء وإرسال الرسالة النصية باسم المُرسل
            message = client.messages.create(
                body=message_body,
                from_="Restart", # استخدام اسم المرسل النصي
                to=phoneNum
            )
            
            msg_sid = message.sid
            # 2. الاستعلام المتكرر (Polling) حتى تستقر حالة الرسالة
            while True:
                time.sleep(1)  # الانتظار لثانية واحدة
                message_details = client.messages(msg_sid).fetch()
                message_status = message_details.status
                # حالات الـ SMS تختلف قليلاً عن الواتساب، أضفنا "sent" لأن بعض شبكات الاتصال لا ترجع حالة "delivered"
                if message_status.lower() in [
                    "delivered",
                    "sent",
                    "failed",
                    "undelivered",
                ]:
                    break

            # 3. تجميع تفاصيل الرسالة بعد استقرار حالتها
            msg_status = message_details.status
            msg_error_code = message_details.error_code
            msg_error_message = message_details.error_message

            contxt = {
                "SID": msg_sid,
                "Status": msg_status,
                "From": message_details.from_,
                "To": message_details.to,
                "Body": message_details.body,
                "Date Sent": message_details.date_sent,
                "Error Code": msg_error_code,
                "Error Message": msg_error_message,
            }
            # 4. تسجيل العملية في قاعدة البيانات (Log)
            messageLog.objects.create(
                To=phoneNum,
                Log=contxt,
                SID=msg_sid,
                Status=msg_status,
                Error_Code=msg_error_code,
                Error_Message=msg_error_message,
            )

            return message_status

    except TwilioRestException as error:
        # تسجيل الخطأ الخاص بـ Twilio في قاعدة البيانات
        messageLog.objects.create(
            To=phoneNum,
            Log=str(error),
            SID=msg_sid,
            Status=msg_status,
            Error_Code=msg_error_code or error.code,
            Error_Message=msg_error_message or error.msg,
        )
        return f"Error: {str(error)}"
    except Exception as e:
        # تسجيل أي أخطاء برمجية أخرى
        messageLog.objects.create(
            To=phoneNum,
            Log=str(e),
            SID=msg_sid,
            Status=msg_status,
            Error_Code=msg_error_code,
            Error_Message=msg_error_message,
        )
        return "failed"


def send_whatsapp_msg(phone, message=None, image_url=None, mimetype="image/jpeg", filename="image.jpg"):
    """
    Sends a WhatsApp message.
    1. Text Only: Pass 'message'.
    2. Image Only: Pass 'image_url' (URL or Base64 Data URI).
    3. Image + Text: Pass 'image_url' and 'message' (message becomes the caption).
    """
    
    # Base configuration
    base_url = "http://82.29.177.121:8001/api"
    headers = {'Content-Type': 'application/json', 'X-Api-Key': 'MoAs@7654'}
    
    # Validation: Ensure we have at least text or an image
    if not message and not image_url:
        return {"status": 400, "result": "No content provided"}

    # --- 1. ROBUST PHONE FORMATTING ---
    try:
        parsed_num = phonenumbers.parse(str(phone), "EG")
        
        if not phonenumbers.is_valid_number(parsed_num):
            return {"status": 400, "result": "Invalid Phone Number"}

        # Format to E.164 (e.g., +32467870650)
        formatted_phone = phonenumbers.format_number(parsed_num, phonenumbers.PhoneNumberFormat.E164)
        
        # Remove the '+' sign (WAHA needs 32467870650)
        clean_phone = formatted_phone.replace('+', '')
        
        
    except phonenumbers.NumberParseException:
        return {"status": 400, "result": "Phone Parse Error"}

    # --- 2. PREPARE PAYLOAD & SELECT ENDPOINT ---
    
    chat_id = f"{clean_phone}@c.us"
    
    if image_url:
        # --- SCENARIO: IMAGE (with or without Text) ---
        url = f"{base_url}/sendImage"
        
        payload = {
            "chatId": chat_id,
            "file": {
                "mimetype": mimetype, 
                "filename": filename,
                "url": image_url
            },
            "caption": message if message else "", # Text becomes the caption
            "session": "default"
        }
    else:
        # --- SCENARIO: TEXT ONLY ---
        url = f"{base_url}/sendText"
        
        payload = {
            "chatId": chat_id,
            "text": message,
            "session": "default"
        }

    # --- 3. SEND ---
    
    log_status = 400
    log_result = ""
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30) # Increased timeout for images
        
        if response.status_code == 201:
            log_status = 200
            log_result = "Sent"
        else:
            log_status = 400
            log_result = response.text
        
    except Exception as e:
        log_status = 500
        log_result = str(e)

    # LOGGING
    # We concatenate image info to the message for the DB log so we don't need to change DB schema
    try:
        
        log_message_content = message if message else ""
        if image_url:
            log_message_content += f" [Image: {image_url}]"

        messageLog.objects.create(
                To=phone,
                Log=log_result,
                SID=phone,
                Status=log_status,
                Error_Code=log_status,
                Error_Message=log_result,
            )
      
    except Exception as log_error:
        messageLog.objects.create(
                To=phone,
                Log=str(log_error),
                SID="",
                Status=500,
                Error_Code=500,
                Error_Message=str(log_error),
            )

    return {"status": log_status, "result": log_result}


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
