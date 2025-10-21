from django.urls import path ,include
from .views import signup ,signin

urlpatterns = [
    path('signup/', signup),
    path('signin/', signin),
]
