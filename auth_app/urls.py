from django.urls import path ,include
from .views import signup ,signin,Profile,verification,enable2FA

urlpatterns = [
    path('signup/', signup),
    path('signin/', signin),
    path('verify-email/', verification),
    path('enable-2fa/', enable2FA),
    path('profile/', Profile.as_view()),
]
