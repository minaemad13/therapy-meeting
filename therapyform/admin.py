from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from therapyform.views import sendAlertMassage, sendMassage
from .resource import ParentsMeetingResource
from .models import MeetingDetails ,ParentsMeeting, messageLog
from django.contrib import messages
from rangefilter.filters import DateRangeFilter
import time


admin.site.site_header = " Restart Your Self"         
admin.site.site_title = "Restart Your Self"           
admin.site.index_title = "Welcome to Rstart admin panel"    
class ParentsMeetingAdmin(ImportExportModelAdmin):
    resource_class = ParentsMeetingResource

    list_display = ('full_name', 'phone_number', 'email', 'creation_Date')
    list_filter = (('creation_Date', DateRangeFilter),)
    search_fields = ('full_name', 'phone_number', 'email')
    actions = ['send_meeting_link', 'send_alert']

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
                        status = sendMassage(obj.phone_number)
                        
                        if status.lower() in ['sent', 'delivered','read']:
                            self.message_user(request, f"Message to {obj.full_name} ({obj.phone_number}) was successfully sent.")
                        if status.lower() in ['failed' ,'undelivered']:
                            self.message_user(request, f"Message to {obj.full_name} ({obj.phone_number}) failed.", level=messages.ERROR)
                except Exception as e:
                    self.message_user(request, f"An error occurred while sending message to {obj.full_name} ({obj.phone_number}): {e}", level=messages.ERROR)

    send_meeting_link.short_description = "Send WhatsApp Meeting Link to Selected Users"

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
                        status = sendAlertMassage(obj.phone_number)
                        if status.lower() in ['sent', 'delivered','read']:
                            self.message_user(request, f"Message to {obj.full_name} ({obj.phone_number}) was successfully sent.")
                        if status.lower() in ['failed' ,'undelivered']:
                            self.message_user(request, f"Message to {obj.full_name} ({obj.phone_number}) failed.", level=messages.ERROR)
                except Exception as e:
                    self.message_user(request, f"An error occurred while sending alert to {obj.full_name} ({obj.phone_number}): {e}", level=messages.ERROR)

    send_alert.short_description = "Send Alert Message to Selected Users"

admin.site.register(ParentsMeeting,ParentsMeetingAdmin)
admin.site.register(MeetingDetails) 
admin.site.register(messageLog) 