from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.sessions.models import Session
from .models import User, Profile
# ======================================================================================================================
# سفارشی‌سازی پنل مدیریت برای مدل کاربر
class CustomUserAdmin(UserAdmin):
    model = User  # تعیین مدل مرتبط با این کلاس ادمین

    # فیلدهای قابل نمایش در لیست کاربران
    list_display = (
        "id",
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
        "is_verified",
    )

    # فیلترهای قابل استفاده در پنل مدیریت
    list_filter = (
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
        "is_verified",
    )

    # فیلدهای قابل جستجو
    search_fields = ("email",)

    # مرتب‌سازی پیش‌فرض کاربران
    ordering = ("email",)

    # دسته‌بندی و نمایش فیلدها در صفحه جزئیات کاربر
    fieldsets = (
        (
            "Authentication",
            {"fields": ("email", "password")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "is_verified",
                    "type",
                )
            },
        ),
        (
            "Group Permissions",
            {"fields": ("groups", "user_permissions")},
        ),
        (
            "Important Date",
            {"fields": ("last_login",)},
        ),
    )

    # تنظیمات فرم ایجاد کاربر جدید در پنل مدیریت
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),  # اعمال استایل عریض به فرم
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                ),
            },
        ),
    )
# ======================================================================================================================
# نمایش اطلاعات سشن‌های کاربران در پنل مدیریت
class SessionAdmin(admin.ModelAdmin):

    # استخراج و نمایش داده‌های رمزگشایی شده سشن
    def _session_data(self, obj):
        return obj.get_decoded()

    list_display = ["session_key", "_session_data", "expire_date"]
# ======================================================================================================================
# ثبت مدل کاربر با تنظیمات سفارشی در پنل مدیریت
admin.site.register(User, CustomUserAdmin)

# ثبت مدل پروفایل در پنل مدیریت
admin.site.register(Profile)

# ثبت مدل سشن‌ها در پنل مدیریت
admin.site.register(Session, SessionAdmin)
# ======================================================================================================================