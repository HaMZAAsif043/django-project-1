from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from auth_app.models import User ,Profile
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.conf import settings
import secrets
from auth_app.utils import send_verification_email
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def signin(req):
    if req.method != 'POST':
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

    try:
        data = json.loads(req.body)
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return JsonResponse({'error': 'Email and password are required'}, status=400)

        user = User.objects.filter(email=email).first()
        if not user:
            return JsonResponse({'error': 'Invalid email or password'}, status=401)

        if not check_password(password, user.password):
            return JsonResponse({'error': 'Invalid email or password'}, status=401)

        refresh = RefreshToken.for_user(user)
        # verification_code = ''.join(secrets.choice('0123456789') for _ in range(6))
        # user.profile.verification_code =verification_code
        # user.profile.save()
        if user.profile.two_factor_auth:
            send_verification_email(user)
            
        return JsonResponse({
                    'message': 'Login successful',
                    'twoStepVerification': user.profile.two_factor_auth,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)