from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.
# AbstractBaseUser를 상속해서 유저 커스텀

# 헬퍼 클래스
class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        """
        주어진 이메일, 비밀번호 등 개인정보로 User 인스턴스 생성
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        """
        주어진 이메일, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여
        """
        superuser = self.create_user(
            email=email,
            password=password,
        )
        
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        
        superuser.save(using=self._db)
        return superuser
    
class User(AbstractBaseUser, PermissionsMixin):
    
    email       = models.EmailField(max_length=30, unique=True, null=True, blank=True)
    nickname    = models.CharField
    phoneNum    = models.CharField
    age         = models.IntegerField
    #True 일 경우 복수 선택 가능하게
    frontEnd    = models.BooleanField
    backEnd     = models.BooleanField
    uiux        = models.BooleanField
    #True 일 경우 복수 선택 가능하게
    mobile      = models.BooleanField
    web         = models.BooleanField
    android     = models.BooleanField
    ios         = models.BooleanField

    # 오픈채팅
    kakao = models.CharField
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

	# 헬퍼 클래스 사용
    objects = UserManager()

	# 사용자의 username field는 email으로 설정 (이메일로 로그인)
    USERNAME_FIELD = 'email'

class Spec(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    spec = models.TextField()

    def __str__(self):
        return self.spec
        