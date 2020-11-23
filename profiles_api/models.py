from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:  # emailがempty stringかno valueの場合
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)  # これで暗号化される。らしい。
        user.save(using=self._db)  # 引数はなくても良いらしいが、将来複数のデータベースを使う時に有効、らしい？

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database Model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)  # Profile情報がアクティブかどうか
    is_staff = models.BooleanField(default=False)  # Staffかどうか（Adminにアクセスできるかどうか）

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'  # デフォルトの必須フィールド
    REQUIRED_FIELDS = ['name']  # 追加の必須フィールド

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of our user"""
        return self.email
