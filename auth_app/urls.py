from django.urls import path ,include
from .views import signup,signin,Profile,verification,enable2FA,forgetPassword,verify_forget_password,reset_password,resend_verification

urlpatterns = [
    path('signup/', signup),
    path('signin/', signin),
    path('verify-email/', verification),
    path('enable-2fa/', enable2FA),
    path('forgetPassword/', forgetPassword),
    path('resend_verification/', resend_verification),
    path('reset_password/', reset_password),
    path('verify_forget_password/', verify_forget_password),
    path('profile/', Profile.as_view()),
]
