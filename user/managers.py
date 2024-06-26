# user/managers.py

from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, password, user_type, superior=None, month_quota=0):
        user = self.model(username=username, user_type=user_type, superior=superior, month_quota=month_quota)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password):
        return self.create_user(username, password, 1)