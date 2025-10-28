# auth_app/utils.py
from django.core.mail import send_mail
import secrets
def send_verification_email(user):
    code = ''.join(secrets.choice('0123456789') for _ in range(6))
    user.profile.verification_code =code
    user.profile.save()
    send_mail(
        'Verify Your Email',
        f'Your verification code is {code}',
        'no-reply@myapp.com',
        [user.email],
    )
