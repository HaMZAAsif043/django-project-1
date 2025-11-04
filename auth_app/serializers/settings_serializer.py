from auth_app.models import Settings
from rest_framework import serializers

class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model =Settings
        fields =[
        'email_notifications',
        'sms_notifications',  
        'marketing_emails', 
        'security_alerts',
        'profile',  
        'push_notifications',
        'account_updates',
        'online_status',
        'privacy_mode',
        # profile_visibility
        'language',
        'timezone',
        'theme']
