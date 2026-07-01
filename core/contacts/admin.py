from django.contrib import admin
from .models import ContactMessageModel
# ======================================================================================================================
# سفارشی‌سازی نمایش پیام‌های تماس در پنل مدیریت
@admin.register(ContactMessageModel)
class ContactMessageAdmin(admin.ModelAdmin):

    # فیلدهای قابل نمایش در لیست پیام‌ها
    list_display = (
        'name',
        'email',
        'message',
        'phone_number',
        'created_date'
    )

    # فیلدهای قابل جستجو در پنل مدیریت
    search_fields = [
        'name',
        'email',
    ]
# ======================================================================================================================