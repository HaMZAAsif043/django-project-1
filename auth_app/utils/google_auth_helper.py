from google.auth.transport import requests
from google.oauth2 import id_token

def verify_google_token(token):
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request())
        print('idinfo',idinfo)
        return idinfo
    except Exception as e:
        print(f"Token verification failed: {e}")
        return None
