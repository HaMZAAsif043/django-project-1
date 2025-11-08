from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from auth_app.models import User, Profile
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

@csrf_exempt
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def enable2FA(req):
    if req.method != 'GET':
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

    try:
        user = req.user
        # import pdb ; pdb.set_trace()
        profile, created = Profile.objects.get_or_create(
            user=user,
        )
        
        profile.two_factor_auth = not profile.two_factor_auth
        profile.save()

        return JsonResponse({
            'message': '2FA updated successfully',
            'two_factor_auth': profile.two_factor_auth
        }, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)