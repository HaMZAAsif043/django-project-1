# auth_app/utils.py
from django.core.mail import send_mail
def send_email(user,code):
    print(user.email)
    send_mail(
        'Verify Your Email',
        f'Your verification code is {code}',
        'no-reply@myapp.com',
        [user.email],
        fail_silently=False,
    )
