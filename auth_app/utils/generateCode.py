from auth_app.models import VerificationCode
import random

def generate_verification_code(profile, purpose):
    code = str(random.randint(100000, 999999))
    verification = VerificationCode.objects.create(profile=profile, code=code, purpose=purpose)
    return verification
