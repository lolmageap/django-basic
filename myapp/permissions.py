from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication

class RoleBasedPermission(BasePermission):
    def has_permission(self, request, view) -> bool:
        auth = JWTAuthentication()

        auth_header = request.headers.get("Authorization")
        if not auth_header: return False

        try:
            token = auth_header.strip("Bearer ")
            validated_token = auth.get_validated_token(token)
        except Exception: return False

        user_roles = validated_token.get("roles", [])
        required_roles = getattr(view, "roles", [])

        return any(role in user_roles for role in required_roles)