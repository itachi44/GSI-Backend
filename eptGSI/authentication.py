from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from rest_framework.authtoken.models import Token


#retourne le temps restant
def expires_in(token):
    time_elapsed = timezone.now() - token.created
    left_time = timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
    return left_time


# vérifie si le token est expiré ou non 
def is_token_expired(token):
    return expires_in(token) < timedelta(seconds = 0)


# si le token est expiré on le supprime
# si le token est expiré on lui crée un nouveau
def token_expire_handler(token):
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
        token = Token.objects.create(user = token.user)
    return is_expired, token

