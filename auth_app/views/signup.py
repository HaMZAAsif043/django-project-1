from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import secrets
from auth_app.models import User, Profile
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction

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

                verification_code =profile.verification_code
                if not profile.verification_code:
                    verification_code = ''.join(secrets.choice('0123456789') for _ in range(6))
                    profile.verification_code = verification_code
                    profile.save()

                send_mail(
                        subject="Email Verification Code",
                        message=f"Your verification code is {verification_code}. It expires in 5 minutes.",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[email],
                        fail_silently=False,
                    )
                return JsonResponse({'message': 'OTP has been resent to your email'}, status=200)

            return JsonResponse({'error': 'Email is already registered'}, status=409)

        with transaction.atomic():
            user = User.objects.create(
                email=email,
                password=make_password(password)
            )

            verification_code = ''.join(secrets.choice('0123456789') for _ in range(6))

            Profile.objects.create(
                user=user,
                username=username,
                dob=dob,
                phone_number=phone_number,
                verification_code=verification_code,
            )

        send_mail(
            subject="Email Verification Code",
            message=f"Your verification code is {verification_code}. It expires in 5 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return JsonResponse({'message': 'OTP has been sent to your email'}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
