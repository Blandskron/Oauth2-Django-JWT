from rest_framework_simplejwt.tokens import RefreshToken

class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)

        # Agregar datos adicionales al token
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["email"] = user.email
        token["is_staff"] = user.is_staff
        token["is_superuser"] = user.is_superuser

        # Si el usuario tiene grupos y permisos
        token["groups"] = list(user.groups.values_list("name", flat=True))  
        token["permissions"] = list(user.user_permissions.values_list("codename", flat=True))  

        return token
