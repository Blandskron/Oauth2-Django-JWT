from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta

class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)

        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["email"] = user.email
        token["is_staff"] = user.is_staff
        token["is_superuser"] = user.is_superuser
        token["groups"] = list(user.groups.values_list("name", flat=True))  
        token["permissions"] = list(user.user_permissions.values_list("codename", flat=True))  

        token.set_exp(lifetime=timedelta(hours=1))

        return token
