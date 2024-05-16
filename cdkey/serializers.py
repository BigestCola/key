# cdkey/serializers.py

from rest_framework import serializers
from .models import CDKey
from django.conf import settings
from .constants import DURATION_CHOICES

class CDKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = CDKey
        fields = ['id', 'key', 'created_at', 'expires_at', 'created_by', 'used_by', 'used_at', 'validity_days', 'is_used_field']

class CDKeyGenerateSerializer(serializers.Serializer):
    duration = serializers.ChoiceField(choices=DURATION_CHOICES)
    count = serializers.IntegerField(min_value=1, max_value=100)

    def save(self, user):
        cdkeys = []
        for _ in range(self.validated_data['count']):
            cdkey = CDKey.generate_cdkey()
            cdkeys.append(CDKey(key=cdkey, validity_days=self.validated_data['duration'], created_by=user))
        CDKey.objects.bulk_create(cdkeys)
        return cdkeys

class CDKeyExtractSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=64)

    def validate_key(self, value):
        try:
            cdkey = CDKey.objects.get(key=value)
        except CDKey.DoesNotExist:
            raise serializers.ValidationError('Invalid CDKey.')
        if cdkey.is_used_field:
            raise serializers.ValidationError('CDKey already used.')
        return cdkey

    def save(self, user):
        cdkey = self.validated_data['key'] 
        cdkey.mark_as_used(user)
        return cdkey

class CDKeyVerifySerializer(serializers.Serializer):
    key = serializers.CharField(max_length=64)
    device_id = serializers.CharField(max_length=255)
    app_version = serializers.CharField(max_length=255)