from django.contrib import admin
from .models import ContactMessageModel, NewsletterSubscriberModel,HistoryItemModel,ProcessStepModel,AwardModel
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
        'user',
        'is_read',
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
# مدیریت سابقه/تاریخچه شرکت
@admin.register(HistoryItemModel)
class HistoryItemModelAdmin(admin.ModelAdmin):

    list_display = ("year", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
# ======================================================================================================================
# مدیریت مراحل کاری
@admin.register(ProcessStepModel)
class ProcessStepModelAdmin(admin.ModelAdmin):

    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
# ======================================================================================================================
# مدیریت جوایز و دستاوردها
@admin.register(AwardModel)
class AwardModelAdmin(admin.ModelAdmin):

    list_display = ("title", "year", "category", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
# ======================================================================================================================