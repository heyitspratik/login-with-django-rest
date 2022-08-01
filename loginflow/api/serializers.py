from rest_framework import serializers
from .models import User, OTPModel, MultipleEmail


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","mobile_number","mobile_verified"]

class MobileLoginOTPGenSerializer(serializers.ModelSerializer):
    mobile_number = serializers.CharField()

    class Meta:
        model = OTPModel
        fields = ("mobile_number",)

class MobileLogInSerializer(serializers.ModelSerializer):
    mobile_number = serializers.CharField()
    otp = serializers.CharField()

    class Meta:
        model = OTPModel
        fields = ("mobile_number", "otp")


class MultipleEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MultipleEmail
        fields = ("user","email","is_primary")