from django.urls import path ,include
from .views import signup ,signin,Profile

urlpatterns = [
    path('signup/', signup),
    path('signin/', signin),
    path('profile/', Profile.as_view()),
]
