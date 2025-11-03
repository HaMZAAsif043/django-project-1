from ..models import Settings
from ..serializers import SettingsSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
class SettingsView(generics.RetrieveUpdateAPIView):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Assuming each user has one settings object linked to their profile
        return Settings.objects.get(profile__user=self.request.user)
