from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from pages.models import NewUsers


class MyBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = NewUsers.objects.get(username=username)
            if user and check_password(password, user.password):
                return user
        except NewUsers.Doesnotexist:
            return None
        