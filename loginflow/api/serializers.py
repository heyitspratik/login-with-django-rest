from rest_framework import serializers
from .models import User, OTPModel, MultipleEmail


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","mobile_number","mobile_verified"]