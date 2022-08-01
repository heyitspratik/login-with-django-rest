from django.urls import path,include
from . import views
from rest_framework import routers

app_name = "drctask_api"

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
      
]

