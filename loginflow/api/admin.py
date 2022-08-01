from django.contrib import admin
from .models import User, OTPModel, MultipleEmail


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_per_page = 10
    search_fields = ('username','mobile_number')
    list_display = ('username','mobile_number','mobile_verified')


@admin.register(OTPModel)
class OTPModelAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ('user','otp')


@admin.register(MultipleEmail)
class MultipleEmailAdmin(admin.ModelAdmin):
    list_per_page = 10
    search_fields = ('user','email')
    list_display = ('user','email','is_primary')
