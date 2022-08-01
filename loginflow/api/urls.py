from django.urls import path,include
from . import views
from rest_framework import routers

app_name = "loginflow_api"

router = routers.DefaultRouter()
router.register(r'signup', views.SignupViewSet)
router.register(r'otpgen', views.MobileLoginOTPGenViewSet)
router.register(r'login', views.MobileLogInViewSet)
router.register(r'emailupdate', views.PrimaryEmailViewSet)

urlpatterns = [
    path('', include(router.urls)),
      
]

