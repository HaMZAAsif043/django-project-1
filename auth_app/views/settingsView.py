from ..models import Settings
from ..serializers import SettingsSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
class SettingsView(APIView):
    queryset = Settings.objects.all()
    serializer_class = SettingsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request):
        # Assuming each user has one settings object linked to their profile
        try:
            setting_instance = Settings.objects.get(profile__user=self.request.user)
            serializer = self.serializer_class(setting_instance)
            return Response(serializer.data)
        except Settings.DoesNotExist:
            return Response({'error': 'Settings not found for this user.'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self,request):
        try:
            setting_instance = Settings.objects.get(profile__user=self.request.user)
            serializer = self.serializer_class(setting_instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Settings.DoesNotExist:
            return Response({'error': 'Settings not found for this user.'}, status=status.HTTP_404_NOT_FOUND)
