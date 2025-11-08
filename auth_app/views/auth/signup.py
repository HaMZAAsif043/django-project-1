from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import secrets
from auth_app.models import User, Profile
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from auth_app.utils import generate_verification_code ,send_email
from django.utils import timezone
@csrf_exempt
def signup(req):
    if req.method != 'POST':
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

    try:
        data = json.loads(req.body)
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        dob = data.get('dob')
        phone_number = data.get('phone_number')

        if not email or not password:
            return JsonResponse({'error': 'Email and password are required'}, status=400)

        user = User.objects.filter(email=email).first()
        import pdb; pdb.set_trace()
        if user:
            if hasattr(user, 'profile'):
                profile = user.profile
                code = profile.codes.filter(is_used=False).first()
                if code.expires_at > timezone.now() and code.is_used ==False:
                    send_email(user,code.code)
                    return JsonResponse({'message': 'OTP has been resent to your email'}, status=200)
                verification  = generate_verification_code(profile=profile ,purpose='ACCOUNT_VERIFY')
                if verification:
                    send_email(user,verification.code)
                    return JsonResponse({'message': 'OTP has been resent to your email'}, status=200)

        with transaction.atomic():
            user = User.objects.create(
                email=email,
                password=make_password(password)
            )

            profile =Profile.objects.create(
                user=user,
                username=username,
                dob=dob,
                phone_number=phone_number,
            )
            verification  = generate_verification_code(profile=profile ,purpose='ACCOUNT_VERIFY')
            if verification:
                send_email(user,verification.code)

        return JsonResponse({'message': 'OTP has been sent to your email'}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
