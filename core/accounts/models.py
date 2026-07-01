from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .validators import validate_iranian_cellphone_number
# ======================================================================================================================
# تعریف نقش‌های مختلف کاربران در سیستم
class UserType(models.IntegerChoices):
    customer = 1, _("customer")
    admin = 2, _("admin")
    superuser = 3, _("superuser")
# ======================================================================================================================
# مدیریت ایجاد کاربران عادی و مدیران سیستم
class UserManager(BaseUserManager):
    # ایجاد و ذخیره کاربر عادی
    def create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError(_("وارد کردن ایمیل الزامی است."))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    # ایجاد و ذخیره کاربر با دسترسی کامل (Superuser)
    def create_superuser(self, email, password, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("type", UserType.superuser.value)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
# ======================================================================================================================
# تعریف مدل سفارشی کاربر با احراز هویت مبتنی بر ایمیل
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    type = models.IntegerField(
        choices=UserType.choices, default=UserType.customer.value
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    # نمایش ایمیل کاربر به عنوان نمای متنی شیء
    def __str__(self):
        return self.email
# ======================================================================================================================
# ذخیره اطلاعات تکمیلی و پروفایل کاربران
class Profile(models.Model):
    user = models.OneToOneField(
        "User", on_delete=models.CASCADE, related_name="user_profile"
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(
        max_length=12, validators=[validate_iranian_cellphone_number]
    )
    image = models.ImageField(
        upload_to="profile/",
        default="profile/default.png",
        blank=True,
        null=True,
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    # بازگرداندن نام کامل کاربر
    def get_fullname(self):
        if self.first_name or self.last_name:
            return self.first_name + " " + self.last_name
        return "کاربر جدید"
# ======================================================================================================================
# ایجاد خودکار پروفایل پس از ساخت کاربر جدید
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, pk=instance.pk)
# ======================================================================================================================