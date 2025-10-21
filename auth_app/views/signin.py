from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from auth_app.models import User ,Profile
from django.contrib.auth.hashers import make_password, check_password

@csrf_exempt
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

        return JsonResponse({'message': 'Login successful'}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)