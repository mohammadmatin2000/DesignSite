from django.db import models
# ======================================================================================================================
# ذخیره پیام‌ها و درخواست‌های ارسالی کاربران از طریق فرم تماس
class ContactMessageModel(models.Model):

    # نام و نام خانوادگی فرستنده
    name = models.CharField(max_length=255)

    # آدرس ایمیل فرستنده
    email = models.EmailField()

    # متن پیام کاربر
    message = models.TextField()

    # شماره تماس فرستنده
    phone_number = models.CharField(max_length=255)

    # نوع خدمت یا درخواست مورد نظر کاربر
    service = models.CharField(max_length=255)

    # تاریخ ایجاد رکورد
    created_date = models.DateTimeField(auto_now_add=True)

    # تاریخ آخرین بروزرسانی رکورد
    updated_date = models.DateTimeField(auto_now=True)

    # نمایش نام فرستنده در پنل مدیریت
    def __str__(self):
        return self.name
# ======================================================================================================================
# ذخیره ایمیل کاربران عضو خبرنامه
class NewsletterSubscriberModel(models.Model):

    # ایمیل کاربر (باید یکتا باشد)
    email = models.EmailField(unique=True)

    # تاریخ عضویت در خبرنامه
    subscribed_date = models.DateTimeField(auto_now_add=True)

    # نمایش ایمیل در پنل ادمین
    def __str__(self):
        return self.email
# ======================================================================================================================