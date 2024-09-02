from django.contrib import admin
from .models import MeetingDetails ,ParentsMeeting, messageLog
# Register your models here.
admin.site.register(ParentsMeeting)
admin.site.register(MeetingDetails) 
admin.site.register(messageLog) 