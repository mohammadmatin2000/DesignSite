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

    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام ها"

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

    class Meta:
        verbose_name = "خبرنامه"
        verbose_name_plural = "خبرنامه ها"

    # نمایش ایمیل در پنل ادمین
    def __str__(self):
        return self.email
# ======================================================================================================================
# مدل آیتم‌های سابقه/تاریخچه شرکت (بخش «درباه ی ما»)
class HistoryItemModel(models.Model):

    # تصویر مربوط به این بازه‌ی زمانی
    image = models.ImageField(
        upload_to="image/history/",
        verbose_name="تصویر"
    )

    # سال (یا بازه‌ی زمانی)
    year = models.CharField(
        max_length=20,
        verbose_name="سال"
    )

    # توضیح کوتاه این رویداد
    description = models.TextField(
        verbose_name="توضیح"
    )

    # ترتیب نمایش در کاروسل
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="ترتیب نمایش"
    )

    # نمایش در سایت
    is_active = models.BooleanField(
        default=True,
        verbose_name="نمایش در سایت"
    )

    class Meta:
        ordering = ["order"]
        verbose_name = "سابقه"
        verbose_name_plural = "سابقه ما"

    def __str__(self):
        return f"{self.year}"
# ======================================================================================================================
# مدل مراحل کاری شرکت (بخش «معماری استثنایی / چگونه کار می کنیم در بخش درباره ی ما»)
class ProcessStepModel(models.Model):

    # تصویر مرحله
    image = models.ImageField(
        upload_to="image/process/",
        verbose_name="تصویر"
    )

    # عنوان مرحله (مثلاً: مشاوره اولیه)
    title = models.CharField(
        max_length=255,
        verbose_name="عنوان"
    )

    # توضیح مرحله
    description = models.TextField(
        verbose_name="توضیح"
    )

    # ترتیب نمایش (همچنین برای شماره‌گذاری 01, 02, ...)
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="ترتیب نمایش"
    )

    # نمایش در سایت
    is_active = models.BooleanField(
        default=True,
        verbose_name="نمایش در سایت"
    )

    class Meta:
        ordering = ["order"]
        verbose_name = "مرحله کاری"
        verbose_name_plural = "مراحل کاری"

    def __str__(self):
        return self.title
# ======================================================================================================================
# مدل جوایز و دستاوردها (بخش «جوایز ما در صنعت در بخش درباه ی ما»)
class AwardModel(models.Model):

    # سال دریافت جایزه
    year = models.CharField(
        max_length=20,
        verbose_name="سال"
    )

    # عنوان جایزه
    title = models.CharField(
        max_length=255,
        verbose_name="عنوان جایزه"
    )

    # دسته‌بندی جایزه (مثلاً: طراحی داخلی، معماری)
    category = models.CharField(
        max_length=255,
        verbose_name="دسته‌بندی"
    )

    # تصویر مرتبط با جایزه (نمایش هنگام هاور روی هر ردیف)
    image = models.ImageField(
        upload_to="image/awards/",
        verbose_name="تصویر"
    )

    # ترتیب نمایش
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="ترتیب نمایش"
    )

    # نمایش در سایت
    is_active = models.BooleanField(
        default=True,
        verbose_name="نمایش در سایت"
    )

    class Meta:
        ordering = ["order"]
        verbose_name = "جایزه"
        verbose_name_plural = "جوایز و دستاوردها"

    def __str__(self):
        return f"{self.title} ({self.year})"
# ======================================================================================================================