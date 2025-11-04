from django.urls import path ,include
from .views import signup,signin,ProfileView,verification,enable2FA,forgetPassword,verify_forget_password,reset_password,resend_verification,google_login,SettingsView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('signup/', signup),
    path('signin/', signin),
    path('verify-email/', verification),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('enable-2fa/', enable2FA),
    path('forgetPassword/', forgetPassword),
    path('resend_verification/', resend_verification),
    path('reset_password/', reset_password),
    path('verify_forget_password/', verify_forget_password),
    path('google_auth/', google_login),
    path('profile/', ProfileView.as_view()),
    path('settings/', SettingsView.as_view()),
]
