from import_export import resources, fields
from .models import ParentsMeeting
import phonenumbers
from phonenumbers import PhoneNumberFormat
class ParentsMeetingResource(resources.ModelResource):

    class Meta:
        model = ParentsMeeting
        
    def before_import_row(self, row, **kwargs):    
        phone_number= row.get('phone_number', None)
        country_code= row.get('country_code', None)
        if phone_number and country_code:
            parsed_number = phonenumbers.parse(str(phone_number), country_code)
            if phonenumbers.is_valid_number(parsed_number):
                formatted_phone_number = phonenumbers.format_number(parsed_number, PhoneNumberFormat.E164)
                row['phone_number'] = formatted_phone_number
            else:
                row['phone_number'] = None
        else:
            row['phone_number'] = None
