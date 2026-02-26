from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from therapyform.views import *
from .resource import ParentsMeetingResource
from .models import MeetingDetails ,ParentsMeeting, messageLog
from django.contrib import messages
from rangefilter.filters import DateRangeFilter
import time
import threading
from django.contrib.admin.helpers import ActionForm
from django import forms
admin.site.site_header = " Restart Your Self"         
admin.site.site_title = "Restart Your Self"           
admin.site.index_title = "Welcome to Rstart admin panel"    




class ParentsMeetingAdmin(ImportExportModelAdmin):
    resource_class = ParentsMeetingResource

    list_display = ('full_name', 'phone_number', 'email', 'creation_Date')
    list_filter = (('creation_Date', DateRangeFilter),)
    search_fields = ('full_name', 'phone_number', 'email')
    actions = ['send_meeting_link','send_Ramadan_msg' ,'send_alert']


    def send_meeting_link(self, request, queryset):
        # Define batch size
        batch_size = 10  # Process 10 rows at a time
        queryset = list(queryset)  # Convert queryset to a list to slice it

        for i in range(0, len(queryset), batch_size):
            batch = queryset[i:i + batch_size]  # Process 10 records in each batch
            for obj in batch:
                try:
                    if obj.phone_number:
                        # Call the sendMassage function and check status
                        threading.Thread(target=sendMassage, args=(obj.phone_number,)).start()
                        # status = sendMassage(obj.phone_number)
                        self.message_user(request, f"Send Massages Run in Background you can check the status of each massage from Message logs.")
                        # if status.lower() in ['sent', 'delivered','read']:
                        #     self.message_user(request, f"Message to {obj.full_name} ({obj.phone_number}) was successfully sent.")
                        # if status.lower() in ['failed' ,'undelivered']:
                        #     self.message_user(request, f"Message to {obj.full_name} ({obj.phone_number}) failed.", level=messages.ERROR)
                except Exception as e:
                    self.message_user(request, f"An error occurred while sending message to {obj.full_name} ({obj.phone_number}): {e}", level=messages.ERROR)

    send_meeting_link.short_description = "Send WhatsApp Meeting Link to Selected Users"

    def send_ramadan_msg(self, request, queryset):
        # Define batch size
        batch_size = 10  # Process 10 rows at a time
        queryset = list(queryset)  # Convert queryset to a list to slice it

        for i in range(0, len(queryset), batch_size):
            batch = queryset[i:i + batch_size]  # Process 10 records in each batch
            for obj in batch:
                try:
                    if obj.phone_number:
                        # Call the sendMassage function and check status
                        threading.Thread(target=sendRamadanMsgGroup, args=(obj.phone_number,)).start()
                        # status = sendMassage(obj.phone_number)
                        self.message_user(request, f"Send Massages Run in Background you can check the status of each massage from Message logs.")
                        # if status.lower() in ['sent', 'delivered','read']:
                        #     self.message_user(request, f"Message to {obj.full_name} ({obj.phone_number}) was successfully sent.")
                        # if status.lower() in ['failed' ,'undelivered']:
                        #     self.message_user(request, f"Message to {obj.full_name} ({obj.phone_number}) failed.", level=messages.ERROR)
                except Exception as e:
                    self.message_user(request, f"An error occurred while sending message to {obj.full_name} ({obj.phone_number}): {e}", level=messages.ERROR)

    send_ramadan_msg.short_description = "Send Ramadan Message to Selected Users"
    
    def send_alert(self, request, queryset):
        # Define batch size
        batch_size = 10  # Process 10 rows at a time
        queryset = list(queryset)  # Convert queryset to a list to slice it

        for i in range(0, len(queryset), batch_size):
            batch = queryset[i:i + batch_size]
            for obj in batch:
                try:
                    if obj.phone_number:
                        # Call the sendAlertMassage function and check status
                        threading.Thread(target=sendAlertMassage, args=(obj.phone_number,)).start()
                        # status = sendMassage(obj.phone_number)
                        self.message_user(request, f"Send Massages Run in Background you can check the status of each massage from Message logs.")
                        # status = sendAlertMassage(obj.phone_number)
                        # if status.lower() in ['sent', 'delivered','read']:
                        #     self.message_user(request, f"Message to {obj.full_name} ({obj.phone_number}) was successfully sent.")
                        # if status.lower() in ['failed' ,'undelivered']:
                        #     self.message_user(request, f"Message to {obj.full_name} ({obj.phone_number}) failed.", level=messages.ERROR)
                except Exception as e:
                    self.message_user(request, f"An error occurred while sending alert to {obj.full_name} ({obj.phone_number}): {e}", level=messages.ERROR)

    send_alert.short_description = "Send Alert Bayot Hadea Message to Selected Users"

# 1. Define your predefined messages here
# PREDEFINED_MESSAGES = {
#     'meeting': """🌟 تأكيد حضور ورشة "كيف تتعامل مع المدمن حتى يقتنع بالعلاج" 🌟

# مرحبًا!

# نشكر لكم تواصلكم معنا سابقًا ويسعدنا تأكيد تسجيلكم في ورشتنا القادمة بعنوان "كيف تتعامل مع المدمن حتى يقتنع بالعلاج"، التي ستقام يوم السبت المقبل بمشاركة الأستاذ سعد المحمود وفريق من المعالجين النفسيين والأخصائيين.

# 📍 المكان: عبر جوجل ميت. يمكنكم الانضمام عبر الرابط التالي: https://rb.gy/w91fdm

# 🕒 الوقت: الساعة الخامسة مساءً بتوقيت السعودية.

# 💬 لأي استفسار أو تواصل إضافي، يمكنكم مراسلتنا عبر الرقم: +962 7 9838 5260""",
#     'ramadan': """🌟 كل عام وانتم بخير بمناسبة حلول شهر رمضان المبارك 🌟
# * نود التنوية الى ان موعد الندوة تغير في شهر رمضان المبارك 

# نشكر لكم تواصلكم معنا سابقًا ويسعدنا تأكيد تسجيلكم في ورشتنا القادمة بعنوان "كيف تتعامل مع المدمن حتى يقتنع بالعلاج"، التي تقام كل يوم سبت بمشاركة الأستاذ سعد المحمود وفريق من المعالجين النفسيين والأخصائيين.

# 📍 المكان: عبر جوجل ميت. يمكنكم الانضمام عبر الرابط التالي: https://rb.gy/w91fdm

# 🕒 الوقت: الساعة ١ ظهرا  بتوقيت السعودية.

# 💬 لأي استفسار أو تواصل إضافي، يمكنكم مراسلتنا عبر الرقم: +962 7 9838 5260""",
#     'alert': """مرحبا معك فريق عيادات ريستارت 

#  الأسبوع القادم من شهر رمضان المبارك رح يبدأ برنامج بيوت هادئه المخصص لأهالي  المدمنين والمتعافين 

# البرنامج لمدة 13 أسبوعاً لدعم وتدريب الأسر التي تواجه تحديات الإدمان، لمساعدتكم على خلق بيئة هادئة وسلمية داخل المنزل مهما كانت الظروف.

# لا يشترط مشاركة المدمن – ابدأ تعافي أسرتك الآن!

# ماذا يتضمن البرنامج؟
# • فهم الإدمان بصورة شاملة وبعيداً عن مشاعر اللوم أو الذنب.
# • تعلم كيفية وضع حدود صحية داخل المنزل بشكل متوازن وآمن.
# • اكتساب مهارات للتعامل مع مشاعر الخوف والغضب والقلق بطريقة واعية.

# تُقدَّم الجلسات الفردية والجماعية بإشراف:
# • الدكتورة أحلام
# • المعالج يونس أبو حشيش

# خبراء دعم الأسر في عيادات ريستارت
# للتواصل والاستفسار على الرقم :
# (wa.me/962778985165)
# +962 7 7898 5165"""
# }

# 2. Create a custom ActionForm with a dropdown
# class WhatsAppActionForm(ActionForm):
#     MESSAGE_CHOICES = [
#         ('', '--- Select a Predefined Message ---'),
#         ('meeting', 'Meeting Link'),
#         ('ramadan', 'Ramadan Meeting Link'),
#         ('alert', 'Alert - Parents Group'),
#     ]
#     message_type = forms.ChoiceField(choices=MESSAGE_CHOICES, required=False)

# # 3. Define a wrapper function for the background thread
# def background_whatsapp_task(phone, message):
#     """Wrapper to call your WAHA function in a thread."""
#     sendSmsAlphanumeric(phoneNum=phone, message_body=message)

# class ParentsMeetingAdmin(ImportExportModelAdmin):
#     resource_class = ParentsMeetingResource
#     list_display = ('full_name', 'phone_number', 'email', 'creation_Date')
#     list_filter = (('creation_Date', DateRangeFilter),)
#     search_fields = ('full_name', 'phone_number', 'email')
    
#     # Override the default action form
#     action_form = WhatsAppActionForm
#     actions = ['send_predefined_whatsapp']

#     def send_predefined_whatsapp(self, request, queryset):
#         # Grab the chosen message type from the dropdown
#         message_key = request.POST.get('message_type')
        
#         if not message_key:
#             self.message_user(request, "Please select a message type from the dropdown.", level=messages.WARNING)
#             return

#         msg_template = PREDEFINED_MESSAGES.get(message_key)
#         batch_size = 10
#         queryset = list(queryset)

#         for i in range(0, len(queryset), batch_size):
#             batch = queryset[i:i + batch_size]
#             for obj in batch:
#                 try:
#                     if obj.phone_number:
#                         # Personalize the message dynamically
#                         personalized_msg = msg_template.format(name=obj.full_name)
                        
#                         # Send to background thread using your new function
#                         threading.Thread(
#                             target=background_whatsapp_task, 
#                             args=(obj.phone_number, personalized_msg)
#                         ).start()
                        
#                 except Exception as e:
#                     self.message_user(request, f"Error queuing message for {obj.full_name}: {e}", level=messages.ERROR)

#         self.message_user(request, "WhatsApp messages are processing in the background. Check logs for delivery status.")

#     send_predefined_whatsapp.short_description = "Send Selected SMS Message"

admin.site.register(ParentsMeeting,ParentsMeetingAdmin)

class messageLogAdmin(admin.ModelAdmin):
    list_display = ('To','SID','Status', 'creation_Date')
    list_filter = (('creation_Date', DateRangeFilter),'Status' )
    search_fields = ('To','SID','Status')
admin.site.register(messageLog,messageLogAdmin) 
admin.site.register(MeetingDetails) 