from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from auth_app.models import User ,Profile
from django.contrib.auth.hashers import make_password, check_password

@csrf_exempt
def profile(req):
    if req.method != 'POST':
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

    try:
        data = json.loads(req.body)
        email = data.get('email')
        # password = data.get('password')

        if not email:
            return JsonResponse({'error': 'Email and password are required'}, status=400)
        import pdb; pdb.set_trace()
        user = User.objects.get(email=email)
        if(user):
            profile = user.profile
        
        if not user:
            return JsonResponse({'error': 'Invalid email or password'}, status=401)

        return JsonResponse({'message': 'Login successful' ,'data': {
        'id': profile.id,
        'email': profile.user.email,
        'name': profile.username,
        'phone': profile.phone_number,
        'dob': profile.dob,
    }}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)