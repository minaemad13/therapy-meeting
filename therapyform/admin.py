from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from therapyform.views import sendAlertMassage, sendMassage
from .resource import ParentsMeetingResource
from .models import MeetingDetails ,ParentsMeeting, messageLog
from django.contrib import messages
from rangefilter.filters import DateRangeFilter


admin.site.site_header = " Restart Your Self"         
admin.site.site_title = "Restart Your Self"           
admin.site.index_title = "Welcome to Rstart admin panel"    
class ParentsMeetingAdmin(ImportExportModelAdmin):
    resource_class = ParentsMeetingResource

    list_display = ('full_name', 'phone_number', 'email', 'creation_Date')
    list_filter = (('creation_Date', DateRangeFilter),)
    search_fields = ('full_name', 'phone_number', 'email')
    actions = ['send_meeting_link','send_alert']

    def send_meeting_link(self, request, queryset):
        for obj in queryset:
            if obj.phone_number:
                # Call the sendMassage function and wait until the message is processed
                status = sendMassage(obj.phone_number)

                # Optional: Show a success message in the admin interface for each processed message
                if status in ['sent', 'delivered']:
                    self.message_user(request, f"Message to {obj.full_name} ({obj.phone_number}) was successfully sent.")
                elif status == 'failed':
                    self.message_user(request, f"Message to {obj.full_name} ({obj.phone_number}) failed.", level=messages.ERROR)

    send_meeting_link.short_description = "Send WhatsApp Meeting Link to Selected Users"
    def send_alert(self, request, queryset):
        for obj in queryset:
            if obj.phone_number:
                # Call the sendMassage function and wait until the message is processed
                status = sendAlertMassage(obj.phone_number)

                # Optional: Show a success message in the admin interface for each processed message
                if status in ['sent', 'delivered']:
                    self.message_user(request, f"Message to {obj.full_name} ({obj.phone_number}) was successfully sent.")
                elif status == 'failed':
                    self.message_user(request, f"Message to {obj.full_name} ({obj.phone_number}) failed.", level=messages.ERROR)

    send_alert.short_description = "Send Alert Message to Selected Users"
    
admin.site.register(ParentsMeeting,ParentsMeetingAdmin)
admin.site.register(MeetingDetails) 
admin.site.register(messageLog) 