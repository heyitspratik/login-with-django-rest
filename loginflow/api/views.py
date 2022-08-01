from django.shortcuts import render
from .models import User, OTPModel, MultipleEmail
from .serializers import UserSerializer, MobileLoginOTPGenSerializer, MobileLogInSerializer, MultipleEmailSerializer
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




class MobileLoginOTPGenViewSet(viewsets.ModelViewSet):
    queryset = OTPModel.objects.all()
    serializer_class = MobileLoginOTPGenSerializer
    http_method_names = ['post']

    def get_user(self, mobile_number):
        try:
            user = User.objects.get(mobile_number=mobile_number)
            return user
        except:
            return 0

    def generate_otp(self, user):
        otp =random.randrange(1000,9999)
        otp_obj = OTPModel.objects.filter(user=user)
        for obj in otp_obj:
            obj.delete()
        OTPModel.objects.create(user=user,otp=otp)
        print("***otp:"+str(otp))
        msg = f"otp for user {user.username} is {otp}"
        logger.info(msg)
        return otp

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            mobile_number = request.data['mobile_number']
            user = self.get_user(mobile_number)
            if user:
                if user.is_active:
                    otp = self.generate_otp(user)
                    mobile_number1 = mobile_number.replace("-", "")
                    mobile_number1 = mobile_number1.replace("+", "")
                    if mobile_number1 and otp:
                        return Response({"status": 1, "message": "OTP sent", "data": {"otp": otp}})
                    else:
                        return Response({"status": 0, "message": "There is some error in otp sending"})
                else:
                    return Response({"status": 0, "message": "You are not an active user."})
            else:
                return Response({"status": 0, "message": "Mobile Number is not registered"})
        if "mobile_number" in serializer.errors:
            return Response({"status": 0, "message": "mobile_number - " + serializer.errors['mobile_number'][0]})
        return Response(serializer.errors)


class MobileLogInViewSet(viewsets.ModelViewSet):
    queryset = OTPModel.objects.all()
    serializer_class = MobileLogInSerializer
    http_method_names = ['post']

    def get_user(self, mobile_number):
        try:
            user = User.objects.get(mobile_number=mobile_number)
            return user
        except:
            return 0

    def verify_otp(self, user, otp):
        try:
            otp_object = OTPModel.objects.get(user=user, otp=otp)
            otp_object.save()
            return 1
        except:
            return 0

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                session_data = request.session['attempts']
            except:
                session_data = None
            try:
                if session_data > 3:
                    return Response({"status": 0, "message": "Too many attempts, please try after 5 minutes."})
            except:
                pass
            mobile_number = request.data['mobile_number']
            otp = request.data['otp']
            user = self.get_user(mobile_number)
            if user:
                status = self.verify_otp(user, otp)
                if status:
                    # if user.is_active and user.email_verified:
                    if user.is_active:
                        try:
                            email_obj = MultipleEmail.objects.get(user=user,is_primary=True)
                            email = email_obj.email
                        except:
                            email = None
                        data = {"user_id": user.id, "email": email, "username": user.username,
                                "mobile_number": user.mobile_number,
                                }
                        return Response({"status": 1, "message": "You have logged in successfully", "data": data})
                    else:
                        return Response({"status": 0, "message": "You are not an active user."})
                else:
                    try:
                        request.session['attempts'] = request.session['attempts'] + 1
                    except:
                        request.session['attempts'] = 1
                    return Response({"status": 0, "message": "OTP incorrect"})
            else:
                return Response({"status": 0, "message": "Mobile Number is not registered"})
        if "mobile_number" in serializer.errors:
            return Response({"status": 0, "message": " mobile_number -" + serializer.errors['mobile_number'][0]})
        if "otp" in serializer.errors:
            return Response({"status": 0, "message": " otp -" + serializer.errors['otp'][0]})
        return Response(serializer.errors)



class PrimaryEmailViewSet(viewsets.ModelViewSet):
    queryset = MultipleEmail.objects.all()
    serializer_class = MultipleEmailSerializer
    http_method_names = ['post']

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.data['user']     # need to pass user id here
            email = request.data['new_email']
            email_obj = MultipleEmail.objects.filter(user__id=user)
            for obj in email_obj:
                obj.is_primary = False
                obj.save()
            try:
                user_obj = User.objects.get(id=user)
            except:
                return Response({"status": 0, "message": "Plese provide valid user id."})
            new_email_obj = MultipleEmail.objects.create(user=user_obj,email=email,is_primary=True)
            data = {"username":new_email_obj.user.username,"email":email,"mobile_number":new_email_obj.user.mobile_number,"is_primary":new_email_obj.is_primary}
            return Response({"status": 1, "message": "Primary email updated successfully", "data": data})

        if "user" in serializer.errors:
            return Response({"status": 0, "message": "user - " + serializer.errors['user'][0]})
        if "email" in serializer.errors:
            return Response({"status": 0, "message": "email - " + serializer.errors['email'][0]})
        return Response(serializer.errors)

