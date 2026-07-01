from django.contrib import admin
from .models import ContactMessageModel, NewsletterSubscriberModel
# ======================================================================================================================
# مدیریت پیام‌های تماس در پنل ادمین
@admin.register(ContactMessageModel)
class ContactMessageAdmin(admin.ModelAdmin):

    # نمایش ستون‌ها در لیست پیام‌ها
    list_display = (
        'name',
        'email',
        'message',
        'phone_number',
        'created_date'
    )

    # امکان جستجو بر اساس این فیلدها
    search_fields = (
        'name',
        'email',
        'phone_number',
    )
# ======================================================================================================================
# مدیریت اعضای خبرنامه در پنل ادمین
@admin.register(NewsletterSubscriberModel)
class NewsletterSubscriberAdmin(admin.ModelAdmin):

    # نمایش ایمیل و تاریخ عضویت
    list_display = (
        'email',
        'subscribed_date',
    )

    # جستجو بر اساس ایمیل
    search_fields = (
        'email',
    )
# ======================================================================================================================