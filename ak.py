import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from user.models import User

username = 'ak'
password = 'akak888'

if User.objects.filter(username=username).exists():
    print(f'管理员用户 {username} 已经存在。')
else:
    User.objects.create_superuser(username=username, password=password)
    print(f'管理员用户 {username} 已成功创建。')