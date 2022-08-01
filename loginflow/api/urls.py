from django.urls import path,include
from . import views
from rest_framework import routers

app_name = "loginflow_api"

router = routers.DefaultRouter()
router.register(r'signup', views.SignupViewSet)

urlpatterns = [
    path('', include(router.urls)),
      
]

