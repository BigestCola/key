# cdkey/serializers.py

from rest_framework import serializers
from .models import CDKey
from django.conf import settings
from .constants import DURATION_CHOICES

class CDKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = CDKey
        fields = ['id', 'cdkey', 'status', 'create_time', 'user', 'extract_time']

class CDKeyGenerateSerializer(serializers.Serializer):
    duration = serializers.ChoiceField(choices=DURATION_CHOICES)
    count = serializers.IntegerField(min_value=1, max_value=100)

    def save(self, user):
        cdkeys = []
        for _ in range(self.validated_data['count']):
            cdkey = CDKey.generate_cdkey()
            cdkeys.append(CDKey(cdkey=cdkey, duration=self.validated_data['duration'], user=user))
        CDKey.objects.bulk_create(cdkeys)
        return cdkeys

class CDKeyExtractSerializer(serializers.Serializer):
    cdkey = serializers.CharField(max_length=64)

    def validate_cdkey(self, value):
        try:
            cdkey = CDKey.objects.get(cdkey=value)
        except CDKey.DoesNotExist:
            raise serializers.ValidationError('Invalid CDKey.')
        if cdkey.status != CDKey.STATUS_UNUSED:
            raise serializers.ValidationError('CDKey already used or expired.')
        return cdkey

    def save(self, user):
        cdkey = self.validated_data['cdkey'] 
        cdkey.status = CDKey.STATUS_USED
        cdkey.extract_time = timezone.now()
        cdkey.user = user
        cdkey.save()
        return cdkey

class CDKeyVerifySerializer(serializers.Serializer):
    cdkey = serializers.CharField(max_length=64)
    device_id = serializers.CharField(max_length=255)
    app_version = serializers.CharField(max_length=20)