from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed 
from .serializers import RegisterSerializer, LoginSerializer
from .tokens import CustomRefreshToken


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

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed("Credenciales inválidas")

        if not user.check_password(password):
            raise AuthenticationFailed("Credenciales inválidas")

        refresh = CustomRefreshToken.for_user(user) 

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })
