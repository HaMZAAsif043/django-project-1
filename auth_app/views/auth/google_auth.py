from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from rest_framework_simplejwt.tokens import RefreshToken
from auth_app.models import User, Profile ,Settings
from auth_app.utils import verify_google_token
import json

@csrf_exempt
def google_login(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
        token = data.get("token")

        if not token:
            return JsonResponse({"error": "Token is required"}, status=400)

        user_data = verify_google_token(token)
        if not user_data:
            return JsonResponse({"error": "Invalid Google token"}, status=400)

        email = user_data.get("email")
        name = user_data.get("name", "Google User")
        picture = user_data.get("picture", "")

        user, created = User.objects.get_or_create(
            email=email,
            defaults={"password": get_random_string(length=12)}
        )
        print(created)
        profile, _ = Profile.objects.get_or_create(
            user=user,
            defaults={"username": name, "profile_img": picture}
        )
        settings =Settings.objects.get_or_create(
            profile =profile
        )
        refresh = RefreshToken.for_user(user)

        return JsonResponse({
            "message": "Login successful",
            "new_user": created,
            "twoStepVerification": profile.two_factor_auth,
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        }, status=200)

    except Exception as e:
        print("❌ Google login error:", e)
        return JsonResponse({"error": str(e)}, status=500)
