from rest_framework import serializers
from django.contrib.auth import get_user_model
from random import randint
from .models import AbstractUser
from django.core.mail import send_mail
# from django.conf import settings


User = get_user_model()
# User = settings.AUTH_USER_MODEL


class UserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=30,
    )
    email = serializers.EmailField(max_length=20)
    password = serializers.CharField(max_length=20, write_only=True)
    confirm_password = serializers.CharField(max_length=15, write_only=True)

    class Meta:
        model = AbstractUser
        fields = [
            "email",
            "otp",
        ]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("username already exists")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "user with this email already exists"
                )
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                "password and confirm_password do not match"
            )
        return super().validate(attrs)

    def create(self, validated_data, *args, **kwargs):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        user.otp = randint(0000, 9999)
        user.is_active = False
        user.save()
        subject = "Activate your account"
        message = f"""
        {user.username} your account has been registered.
        otp for activating your account is {user.otp}
        """

        email_from = "myims@gmail.com"

        recipient_list = [
            user.email,
        ]
        send_mail(
            subject,
            message,
            email_from,
            recipient_list,
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UserActivationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()


# class ForgetPasswordSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     current_password = serializers.CharField()
#     new_password = serializers.CharField()
