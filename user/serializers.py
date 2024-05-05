# user/serializers.py

from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'user_type', 'superior', 'status', 'month_quota']

class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=32)
    password = serializers.CharField(max_length=128, write_only=True)  
    user_type = serializers.ChoiceField(choices=User.USER_TYPE_CHOICES)
    day_quota = serializers.IntegerField(min_value=0, required=False) 
    month_quota = serializers.IntegerField(min_value=0, required=False)


    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Username already exists.')
        return value

    def validate(self, data):
        if data['user_type'] == User.TYPE_AGENT2 and 'month_quota' not in data:
            raise serializers.ValidationError('Month quota is required for agent2.')
        return data

    def save(self, superior=None):
        user = User.objects.create_user(
            username=self.validated_data['username'],
            password=self.validated_data['password'],
            user_type=self.validated_data['user_type'],
            superior=superior,
            day_quota=self.validated_data.get('day_quota', 0),
            month_quota=self.validated_data.get('month_quota', 0), 
        )
        return user

class UserUpdateSerializer(serializers.Serializer):
    status = serializers.BooleanField(required=False)
    day_quota = serializers.IntegerField(min_value=0, required=False)
    month_quota = serializers.IntegerField(min_value=0, required=False)

    def update(self, instance, validated_data):
        instance.day_quota = validated_data.get('day_quota', instance.day_quota)
        instance.month_quota = validated_data.get('month_quota', instance.month_quota)
        instance.save()
        return instance