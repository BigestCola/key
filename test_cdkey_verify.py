import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from cdkey.views import CDKeyVerifyView
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth import get_user_model

User = get_user_model()

def test_cdkey_verify():
    factory = APIRequestFactory()
    view = CDKeyVerifyView.as_view()

    # 创建一个测试用户
    user = User.objects.create_user(username='testuser', password='testpassword')

    # 创建测试请求数据
    data = {
        'cdkey': 'your_cdkey',
        'device_id': 'your_device_id',
        'app_version': 'your_app_version'
    }

    print(f"Request data: {data}")  # 打印请求数据

    # 创建POST请求
    request = factory.post('/cdkey/verify/', data, format='json')

    # 使用测试用户强制进行身份验证
    force_authenticate(request, user=user)

    # 调用视图并获取响应
    response = view(request)

    print(f"Response data: {response.data}")  # 打印响应数据
    print(f"Response status code: {response.status_code}")  # 打印响应状态码

    # 检查响应状态码
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # 检查响应数据
    assert 'status' in response.data, "Response data does not contain 'status'"
    assert response.data['status'] == 1, f"Expected status 1, but got {response.data['status']}"

if __name__ == '__main__':
    test_cdkey_verify()