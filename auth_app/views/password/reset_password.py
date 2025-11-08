from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import secrets
from auth_app.models import User, Profile
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from django.contrib.auth.password_validation import validate_password
from auth_app.utils import generate_verification_code ,send_email

@csrf_exempt
def reset_password(req):
    if req.method != 'POST':
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

    try:
        data = json.loads(req.body)
        email = data.get('email')
        password = data.get('password')
        

        if not email:
            return JsonResponse({'error': 'Invalid Email'}, status=400)
        if not password:
            return JsonResponse({'error': 'Invalid Password'}, status=400)

        user = User.objects.filter(email=email).first()
        import pdb; pdb.set_trace();
        if user:
            if hasattr(user, 'profile'):
                profile = user.profile
                if profile.forget_password == True:
                    try:
                        validate_password(password) 
                    except ValidationError as e:
                        return Response({'error': list(e.messages)}, status=400)
                    user.password = make_password(password)
                    user.save()
                    return JsonResponse({'message': 'Password Reset Successful'}, status=200)
                return JsonResponse({'error': 'Not authenticated to perform this action'}, status=401)



            return JsonResponse({'error': 'User Not Found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)