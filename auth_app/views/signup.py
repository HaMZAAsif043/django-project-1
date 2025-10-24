from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from auth_app.models import User, Profile
from django.contrib.auth.hashers import make_password
import secrets
from django.core.mail import send_mail
from django.conf import settings

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

        # --- Validation ---
        if not email or not password:
            return JsonResponse({'error': 'Email and password are required'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=409)

        # --- Create user ---
        user = User.objects.create(
            email=email,
            password=make_password(password)
        )

        # --- Generate 6-digit OTP ---
        verification_code = ''.join(secrets.choice('0123456789') for _ in range(6))

        # --- Create profile ---
        Profile.objects.create(
            phone_number=phone_number,
            dob=dob,
            user=user,
            username=username,
            verification_code=verification_code
        )

        send_mail(
            subject="Email Verification Code",
            message=f"Your verification code is {verification_code}. It expires in 5 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return JsonResponse({'message': 'OTP has been sent to your email'}, status=201)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
