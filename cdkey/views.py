# cdkey/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CDKey, CDKeyExtractRecord
from user.permissions import IsAdmin, IsAgent
from django.utils import timezone
from .serializers import CDKeySerializer, CDKeyGenerateSerializer, CDKeyExtractSerializer, CDKeyVerifySerializer
from user.models import User
import requests
from rest_framework.permissions import AllowAny


class CDKeyGenerateView(APIView):
    permission_classes = [IsAdmin | IsAgent]

    def post(self, request):
        serializer = CDKeyGenerateSerializer(data=request.data)
        if serializer.is_valid():
            cdkeys = serializer.save(user=request.user)
            return Response(CDKeySerializer(cdkeys, many=True).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CDKeyExtractView(APIView):
    def post(self, request):
        serializer = CDKeyExtractSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            today = timezone.now().date()

            # 检查每日配额
            if user.cdkeys.filter(extract_time__date=today).count() >= user.day_quota:
                return Response({'error': 'Daily quota exceeded.'}, status=status.HTTP_403_FORBIDDEN)

            # 检查每月配额
            if user.quota_updated_at.month != today.month:
                user.month_quota = user.month_quota_limit
                user.quota_updated_at = today
                user.save()
            if user.cdkeys.filter(extract_time__month=today.month).count() >= user.month_quota:
                return Response({'error': 'Monthly quota exceeded.'}, status=status.HTTP_403_FORBIDDEN)

            cdkey = serializer.save(user=user)
            return Response(CDKeySerializer(cdkey).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CDKeyQueryView(APIView):
    permission_classes = [AllowAny] 

    def get(self, request):
        cd_key = request.query_params.get('cd_key')
        if cd_key:
            try:
                cdkey = CDKey.objects.get(key=cd_key)
                return Response(CDKeySerializer(cdkey).data)
            except CDKey.DoesNotExist:
                return Response({"error": "Invalid CDKey"}, status=400)
        else:
            return Response({"error": "CDKey parameter is required"}, status=400)

class CDKeyVerifyView(APIView):
    def post(self, request):
        serializer = CDKeyVerifySerializer(data=request.data)
        if serializer.is_valid():
            cdkey_text = serializer.validated_data['cdkey']
            device_id = serializer.validated_data['device_id']
            app_version = serializer.validated_data['app_version']

            # TODO: 验证请求签名

            try:
                cdkey = CDKey.objects.get(key=cdkey_text)
            except CDKey.DoesNotExist:
                return Response({'status': 0, 'error': 'Invalid CDKey'}, status=status.HTTP_400_BAD_REQUEST)

            if cdkey.is_used_field:
                return Response({'status': 0, 'error': 'CDKey already used'}, status=status.HTTP_400_BAD_REQUEST)

            if cdkey.expires_at < timezone.now():
                return Response({'status': 0, 'error': 'CDKey expired'}, status=status.HTTP_400_BAD_REQUEST)

            if cdkey.used_by != request.user:
                return Response({'status': 0, 'error': 'CDKey does not belong to the authenticated user'}, status=status.HTTP_403_FORBIDDEN)

            # 更新CDKey的状态和提取时间
            cdkey.mark_as_used(request.user)

            # 记录用户提取CDKey的设备信息和应用版本
            CDKeyExtractRecord.objects.create(
                cdkey=cdkey,
                device_id=device_id,
                app_version=app_version
            )

            return Response({'status': 1, 'expire_time': cdkey.expires_at}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def make_request(url, token):
    try:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 如果响应状态码不是200,则抛出异常
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"

def main():
    url = "http://192.168.3.87:8200/cdkey/"
    token = "your_jwt_token_here"  # 将此替换为你的实际 JWT Token
    response = make_request(url, token)
    print("Server response:", response)

if __name__ == "__main__":
    main()
