from django.contrib import admin
from .models import User, Spec

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'nickname', 'phoneNum', 'age', 'profile_picture', 'frontEnd', 'backEnd', 'uiux',
                    'mobile', 'web', 'android', 'ios', 'mbti', 'kakao', 'is_superuser', 'is_active', 'is_staff')
    list_filter = ('frontEnd', 'backEnd', 'uiux', 'mobile', 'web', 'android', 'ios')
    search_fields = ('email', 'nickname')

@admin.register(Spec)
class SpecAdmin(admin.ModelAdmin):
    list_display = ('user', 'spec')
