from django.db import models
from .Profile import Profile

class Settings(models.Model):
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    marketing_emails =models.BooleanField(default=False)
    security_alerts= models.BooleanField(default=True)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="settings")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    push_notifications = models.BooleanField(default=False)
    account_updates =models.BooleanField(default=False)
    online_status =models.BooleanField(default=False)
    privacy_mode =models.BooleanField(default=False)
    # profile_visibility =
    language = models.CharField(max_length=50, default="English")
    timezone = models.CharField(max_length=50, default='Asia/Karachi')
    theme =models.CharField(max_length=50, default='light')
    def __str__(self):
        return str(self.profile.username)
    class Meta:
        db_table = 'user_settings'
        verbose_name = 'User Setting'
        verbose_name_plural = 'User Settings'