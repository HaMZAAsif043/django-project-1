from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from auth_app.models import Profile


class Profile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user  
            profile = user.profile

            return Response({
                'id': profile.id,
                'email': user.email,
                'name': profile.username,
                'phone': profile.phone_number,
                'dob': profile.dob,
                'profile_img': profile.profile_img.url if profile.profile_img else None,
            }, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            user = request.user
            profile = user.profile

            username = request.data.get("username")
            phone_number = request.data.get("phone_number")
            profile_img = request.data.get("profile_img")

            if username:
                profile.username = username
            if phone_number:
                profile.phone_number = phone_number
            if profile_img:
                profile.profile_img = profile_img

            profile.save()
            return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
