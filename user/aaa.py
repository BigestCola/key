from cdkey.views import CDKeyVerifyView
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth.models import User

def test_cdkey_verify():    
    factory = APIRequestFactory()
    view = CDKeyVerifyView.as_view()

    # 创建一个测试用户
    user = User.objects.create_user(username='testuser', password='testpassword')

    # 创建测试请求数据
    data = {
        'cdkey': 'aa14682d-8a30-4e7d-b8ce-65b0faa80b3c',
        'device_id': 'your_device_id',
        'app_version': 'your_app_version'
    }

    # 创建POST请求
    request = factory.post('/cdkey/verify/', data, format='json')

    # 使用测试用户强制进行身份验证
    force_authenticate(request, user=user)

    # 调用视图并获取响应
    response = view(request)

    # 打印响应数据
    print(response.data)

    # 检查响应状态码
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # 检查响应数据
    assert 'status' in response.data, "Response data does not contain 'status'"
    assert response.data['status'] == 1, f"Expected status 1, but got {response.data['status']}"

# 运行测试
test_cdkey_verify()
