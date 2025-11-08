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
from auth_app.models import VerificationCode
from django.utils import timezone


@csrf_exempt
def verification(req):
    if req.method != 'POST':
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

    try:
        data = json.loads(req.body)
        email = data.get('email')
        code = data.get('code')
        purpose = data.get('purpose')
        

        if not email:
            return JsonResponse({'error': 'Invalid Email'}, status=400)
        if  not code:
            return JsonResponse({'error': 'Invalid Verification Code'}, status=400)

        user = User.objects.filter(email=email).first()
        import pdb; pdb.set_trace()
        if user:
            if hasattr(user, 'profile'):
                profile = user.profile

                verification_code = VerificationCode.objects.filter(profile=profile,code=code ,purpose=purpose or 'ACCOUNT_VERIFY',is_used=False).first()
                if verification_code.code == code and verification_code.expires_at > timezone.now():
                    user.profile.isActive =True
                    verification_code.is_used=True
                    if purpose == 'FORGOT_PASSWORD':
                        profile.forget_password =True
                        profile.save()
                        return JsonResponse({'message': 'Verified Successful',} ,status=200)
                    verification_code.save()
                    refresh = RefreshToken.for_user(user)

                    return JsonResponse({'message': 'Verified successful',
                                         'tokens': {
                                             'refresh': str(refresh),
                                             'access': str(refresh.access_token),
                                            }} ,status=200)
                return JsonResponse({'error': 'Code Expired'}, status=400)

        return JsonResponse({'error': 'User Not Found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
