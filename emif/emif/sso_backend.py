
import django.core.validators
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.conf import settings
from userena.utils import get_user_model

class SSOBackend(object):
    User = get_user_model()
    def authenticate(self, username=None, password=None, check_password=True):

        print username
        print password
        if password==settings.SECRET_KEY:
            print ("entrou")
            user = None;
            try:
                django.core.validators.validate_email(username)
                try: user = User.objects.get(email__iexact=username)
                except User.DoesNotExist: return None
            except django.core.validators.ValidationError:
                try: user = User.objects.get(username__iexact=username)
                except User.DoesNotExist: return None

            return user

        return None

    def get_user(self, user_id):
        User = get_user_model()
        try: return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None