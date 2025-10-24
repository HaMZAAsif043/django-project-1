from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from auth_app.models import User ,Profile
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

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

        return JsonResponse({
                    'message': 'Login successful',
                    'user': {
                        'id': user.id,
                        'username': user.profile.username,
                        'email': user.email,
                    },
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)