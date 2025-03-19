from django.urls import path
from .views import RegisterView, LoginView, ProfileView, oauth_callback	

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('callback/', oauth_callback, name='oauth_callback'),
]
