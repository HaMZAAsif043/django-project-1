from django.db import models
from django.utils import timezone
from datetime import timedelta
from .User import User
from .Profile import Profile  # your existing model

class VerificationCode(models.Model):
    PURPOSE_CHOICES = [
        ('2FA', 'Two-Factor Authentication'),
        ('FORGOT_PASSWORD', 'Forgot Password'),
        ('ACCOUNT_VERIFY', 'Account Verification'),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='codes')
    code = models.CharField(max_length=6)
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    is_used = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.profile.username} - {self.purpose}"
