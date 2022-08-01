from django.shortcuts import render
from .models import User, OTPModel, MultipleEmail
from .serializers import UserSerializer
from rest_framework import viewsets
from rest_framework.response import Response
import random
import logging
logger = logging.getLogger(__name__)


class SignupViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post']

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = request.data['username']
            email = request.data['email']
            password = request.data['password']
            mobile_number = request.data['mobile_number']
            user = User.objects.create_user(username=username, password=password, mobile_number=mobile_number, is_active=True)
            email_created = MultipleEmail.objects.create(user=user, email=email)
            data = {"user_id":user.id,"username":username, "email":email, "mobile_number":mobile_number,"mobile_verified":user.mobile_verified}
            if email_created:
                print("Congrats, Account created successfully")
                return Response(
                    {"status": 1, "message": "Congrats, Account created successfully", "data": data})
            else:
                return Response({"status": 1, "message": "Something went wrong!."})
        if "username" in serializer.errors:
            return Response({"status": 0, "message": "username - " + serializer.errors['username'][0]})
        if "email" in serializer.errors:
            if serializer.errors['email'][0] == "user with this email address already exists.":
                return Response({"status": 0, "message": "Email is already registered"})
            return Response({"status": 0, "message": "email - " + serializer.errors['email'][0]})
        if "password" in serializer.errors:
            return Response({"status": 0, "message": "passowrd - " + serializer.errors['password'][0]})
        if "mobile_number" in serializer.errors:
            return Response({"status": 0, "message": "mobile_number - " + serializer.errors['mobile_number'][0]})
        return Response(serializer.errors)

