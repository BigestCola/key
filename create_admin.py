import os
import django
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from user.models import User

class UserManager(BaseUserManager):
    def create_user(self, username, password, user_type, superior=None, month_quota=0):
        user = self.model(username=username, user_type=user_type, superior=superior, month_quota=month_quota)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password, 1)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user

class User(AbstractBaseUser):
    USER_TYPE_CHOICES = (
        (1, '管理员'),
        (2, '一级代理'),
        (3, '二级代理'),
    )

    username = models.CharField(max_length=32, unique=True)
    user_type = models.SmallIntegerField(choices=USER_TYPE_CHOICES)
    superior = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')
    status = models.BooleanField(default=True)
    day_quota = models.IntegerField(default=0)
    month_quota = models.IntegerField(default=0)
    quota_updated_at = models.DateField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'user'

username = 'akak'
password = 'Editedit88*'

if User.objects.filter(username=username).exists():
    print(f'管理员用户 {username} 已经存在。')
else:
    User.objects.create_superuser(username, password)
    print(f'管理员用户 {username} 已成功创建。')