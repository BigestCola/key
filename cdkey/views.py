# cdkey/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CDKey
from .serializers import CDKeySerializer, CDKeyGenerateSerializer, CDKeyExtractSerializer
from user.permissions import IsAdmin, IsAgent
from django.utils import timezone
from .serializers import CDKeyVerifySerializer
from django.utils import timezone
from .serializers import CDKeySerializer, CDKeyGenerateSerializer, CDKeyExtractSerializer, CDKeyVerifySerializer

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
            cdkey = serializer.save(user=request.user)
            return Response(CDKeySerializer(cdkey).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CDKeyQueryView(APIView):
    def get(self, request):
        cdkeys = request.user.cdkeys.all()
        return Response(CDKeySerializer(cdkeys, many=True).data)



class CDKeyVerifyView(APIView):
    def post(self, request):
        serializer = CDKeyVerifySerializer(data=request.data)
        if serializer.is_valid():
            cdkey = serializer.validated_data['cdkey']
            device_id = serializer.validated_data['device_id']
            app_version = serializer.validated_data['app_version']

            # TODO: 验证请求签名

            try:
                cdkey = CDKey.objects.get(cdkey=cdkey)
            except CDKey.DoesNotExist:
                return Response({'status': 0, 'error': 'Invalid CDKey'}, status=status.HTTP_400_BAD_REQUEST)

            if cdkey.status != 1:
                return Response({'status': 0, 'error': 'Invalid CDKey'}, status=status.HTTP_400_BAD_REQUEST)

            if cdkey.expire_time < timezone.now():
                return Response({'status': 0, 'error': 'CDKey expired'}, status=status.HTTP_400_BAD_REQUEST)

            # TODO: 验证device_id和app_version

            # TODO: 记录CDKey使用情况

            return Response({'status': 1, 'expire_time': cdkey.expire_time}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)