from rest_framework.permissions import BasePermission
from .authentication import *

class IsStudentAuthenticated(BasePermission):
 
    def has_permission(self, request, view):
    # accès aux utilisateurs étudiants authentifiés
    #Tester si l'utilisateur qui demande la page n'est pas un utilisatreur anonyme
        if request.user.is_anonymous:
            return bool(False)
        else:
            token, _ = Token.objects.get_or_create(user = request.user)
            is_expired = is_token_expired(token) 
            if(is_expired):
                token.delete()
                request.user.is_authenticated=False
                return bool(False)
            else:
                return bool(request.user and request.user.is_authenticated and request.user.has_perm("eptGSI.is_student") and not is_expired)