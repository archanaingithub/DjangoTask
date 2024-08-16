# from django.shortcuts import render
from rest_framework import mixins, viewsets
from .serializers import UserRegisterSerializer
from django.contrib.auth import get_user_model, authenticate
from rest_framework.response import Response
# from django.contrib.auth.hashers import make_password, check_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import action
from .serializers import UserRegisterSerializer, UserLoginSerializer


# Create your views here

User = get_user_model()


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    @swagger_auto_schema(
        methods=["POST"],
        request_body=UserLoginSerializer,
    )
    @action(
        detail=False,
        methods=["POST"],
    )
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "user": serializer.data,
                    "token": token.key,
                }
            )
        return Response(
            {"details": "invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )