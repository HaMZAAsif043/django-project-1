from django.urls import path ,include
from .views import signup,signin,ProfileView,verification,enable2FA,forgetPassword,verify_forget_password,reset_password,resend_verification,google_login,SettingsView

urlpatterns = [
    path('signup/', signup),
    path('signin/', signin),
    path('verify-email/', verification),
    path('enable-2fa/', enable2FA),
    path('forgetPassword/', forgetPassword),
    path('resend_verification/', resend_verification),
    path('reset_password/', reset_password),
    path('verify_forget_password/', verify_forget_password),
    path('google_auth/', google_login),
    path('profile/', ProfileView.as_view()),
    path('settings/', SettingsView.as_view()),
]
