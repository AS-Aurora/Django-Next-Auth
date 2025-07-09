from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from allauth.account.models import EmailAddress

class CustomLoginSerializer(LoginSerializer):
    def validate(self, attrs):
        validated_data = super().validate(attrs)

        user = self.user
        if not EmailAddress.objects.filter(user=user, verified=True).exists():
            raise serializers.ValidationError("Email address is not verified.")
    
        return validated_data