from django.db import models
from .User import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="profile")
    profile_img = models.TextField(null=True, blank=True)  
    phone_number = models.CharField(max_length=11, unique=True)
    dob = models.DateField()
    username = models.CharField(max_length=20,null=False,default='default_username')
    created_at = models.DateTimeField(auto_now_add=True)
    isActive =models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, default='')
    two_factor_auth = models.BooleanField(default=False)
    forget_password =models.BooleanField(default=False)
    is_Bloked = models.BooleanField(default=False)
    class Meta:
        db_table = 'user_profiles'  
        ordering = ['-created_at']  
        unique_together = ('user', 'phone_number') 
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    def __str__(self):
        return self.username