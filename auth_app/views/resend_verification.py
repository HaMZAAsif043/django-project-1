from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from auth_app.models import User, VerificationCode
from ..utils import generate_verification_code, send_email


@csrf_exempt
def resend_verification(req):
    if req.method != 'POST':
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

    try:
        data = json.loads(req.body)
        email = data.get('email')
        purpose = data.get('purpose', 'ACCOUNT_VERIFY')

        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)

        user = User.objects.filter(email=email).first()
        if not user:
            return JsonResponse({'error': 'User not found'}, status=404)

        if not hasattr(user, 'profile'):
            return JsonResponse({'error': 'Profile not found for this user'}, status=404)

        profile = user.profile

        # Check if an unexpired, unused code exists
        existing_code = VerificationCode.objects.filter(
            profile=profile,
            purpose=purpose,
            is_used=False,
            expires_at__gt=timezone.now()
        ).first()

        if existing_code:
            # Reuse the same valid code
            send_email(user, existing_code.code)
            return JsonResponse({'message': 'Verification code resent to your email'}, status=200)

        # Otherwise, generate a new one
        new_code = generate_verification_code(profile, purpose)
        send_email(user, new_code.code)

        return JsonResponse({'message': 'New verification code sent to your email'}, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
