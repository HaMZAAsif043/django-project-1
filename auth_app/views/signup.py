from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from auth_app.models import User ,Profile
from django.contrib.auth.hashers import make_password, check_password

@csrf_exempt
def signup(req):
    if req.method != 'POST':
        return HttpResponse('Method Not Allowed',status=405)
    try:
        data =json.loads(req.body)
        email = data.get('email')
        username =data.get('username')
        user_id = data.get('user_id')
        password = data.get('password')
        dob =data.get('dob')
        phone_number =data.get('phone_number')

        if not email:
            return HttpResponse("Email is Required",status=400)
        if User.objects.filter(email=email).first():
            return HttpResponse("Email Already Exist",status=409)

        user = User.objects.create(
            email=email,
            password=make_password(password)
        )
        if user:
            profile= Profile.objects.create(
                phone_number=phone_number,
                dob =dob,
                user =user,
                username =username
            )
            
    except Exception as e:
        return HttpResponse(str(e),status=400)
    return HttpResponse("Profile created successful",status=201 )