from rest_framework import serializers
from crmapp.models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [ 'id',
            'branch',
            'first_name',
            'last_name',
            'primary_email',
            'office_phone',
            'organization_name',
            'mobile_phone',
            'home_phone',
            'secondary_phone',
            'fax',
            'date_of_birth',
            'reports_to',
            'secondary_email',
            'assigned_to',
            'lead_source',
            'support_start_date',
            'support_end_date',
            'mailing_street',
            'mailing_city',
            'mailing_state',
            'mailing_zip',
            'mailing_country',
            'description',
            'profile_picture',
            'created_by',
            ]