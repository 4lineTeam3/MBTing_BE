from django.contrib import admin
from .models import User

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'nickname', 'phoneNum', 'age', 'profile_picture', 'frontEnd', 'backEnd', 'uiux',
                    'mobile', 'web', 'android', 'ios', 'mbti','spec1','spec2','spec3','spec4', 'kakao', 'is_superuser', 'is_active', 'is_staff')
    list_filter = ('frontEnd', 'backEnd', 'uiux', 'mobile', 'web', 'android', 'ios')
    search_fields = ('email', 'nickname')