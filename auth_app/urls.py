from django.urls import path ,include
from .views import signup ,signin,profile

urlpatterns = [
    path('signup/', signup),
    path('signin/', signin),
    path('profile/', profile),
]
