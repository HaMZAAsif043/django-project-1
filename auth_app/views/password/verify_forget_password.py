from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import secrets
from auth_app.models import User, Profile
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken

@csrf_exempt
def verify_forget_password(req):
    if req.method != 'POST':
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

    try:
        data = json.loads(req.body)
        email = data.get('email')
        code = data.get('code')
        

        if not email:
            return JsonResponse({'error': 'Invalid Email'}, status=400)
        if  not code:
            return JsonResponse({'error': 'Invalid Verification Code'}, status=400)

        user = User.objects.filter(email=email).first()
        # import pdb; pdb.set_trace()
        if user:
            if hasattr(user, 'profile'):
                profile = user.profile

                verification_code = profile.verification_code
                if verification_code == code:
                    user.profile.isActive =True
                    user.profile.verification_code=''
                    user.profile.forget_password = True
                    user.profile.save()
                    refresh = RefreshToken.for_user(user)

                    return JsonResponse({'message': 'Verified Successful',} ,status=200)


            return JsonResponse({'error': 'User Not Found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
