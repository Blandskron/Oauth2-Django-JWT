import random
import string
import base64
import hashlib
import requests
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import RegisterSerializer, UserSerializer, LoginSerializer	
from django.http import JsonResponse
from .tokens import CustomRefreshToken 

# Generación de code_verifier
def generate_code_verifier():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))

# Generación de code_challenge
def generate_code_challenge(code_verifier):
    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    return base64.urlsafe_b64encode(code_challenge).decode('utf-8').replace('=', '')

def oauth_callback(request):
    # Capturamos el código de autorización (authorization code)
    authorization_code = request.GET.get('code')

    if not authorization_code:
        return JsonResponse({'error': 'No authorization code provided'}, status=400)

    # Obtener el code_verifier de la sesión (esto debería haberse guardado previamente)
    code_verifier = request.session.get('code_verifier')

    if not code_verifier:
        return JsonResponse({'error': 'No code_verifier found'}, status=400)

    # Solicitud POST para intercambiar el código por el token
    token_url = 'http://127.0.0.1:8000/o/token/'

    token_data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': 'http://127.0.0.1/callback',  # Debe coincidir con la URL de redirección configurada
        'client_id': 'eY3vjQHtBS6SbtZuk5oSmgIo36IYooClxqTE7njB',
        'client_secret': 'pbkdf2_sha256$870000$K2C88Oa51JEPxMbCnHLRar$tWIUcc92YG9olBqZZeLHy2FOMXBjqmmR1ehm/1kn5OE=',
        'code_verifier': code_verifier
    }

    response = requests.post(token_url, data=token_data)

    if response.status_code == 200:
        tokens = response.json()
        return JsonResponse(tokens)  # Retorna el access_token y refresh_token
    else:
        return JsonResponse({'error': 'Failed to obtain token'}, status=400)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer 

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = User.objects.filter(email=email).first()

        if user and user.check_password(password):
            refresh = CustomRefreshToken.for_user(user) 

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })
        return Response({"error": "Credenciales inválidas"}, status=400)

class ProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
