from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import secrets
from auth_app.models import User, Profile
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from auth_app.utils import send_verification_email

@csrf_exempt
def forgetPassword(req):
    if req.method != 'POST':
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

    try:
        data = json.loads(req.body)
        email = data.get('email')
        

        if not email:
            return JsonResponse({'error': 'Invalid Email'}, status=400)
    

        user = User.objects.filter(email=email).first()
        if user:
            if hasattr(user, 'profile'):
                profile = user.profile
                send_verification_email(user)

                return JsonResponse({'message': 'Mail sent successful'},status=200)


            return JsonResponse({'error': 'User Not Found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
