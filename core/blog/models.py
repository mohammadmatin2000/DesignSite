from django.db import models
from django.utils.text import slugify
# ======================================================================================================================
# مدل دسته‌بندی مقالات
class CategoryModels(models.Model):

    # عنوان دسته‌بندی
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    # نمایش عنوان دسته‌بندی
    def __str__(self):
        return self.title
# ======================================================================================================================
# مدل برچسب‌های مقالات
class TagModel(models.Model):

    # عنوان برچسب
    title = models.CharField(max_length=100)

    # اسلاگ برچسب (برای لینک صفحه‌ی فیلتر بر اساس برچسب)
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True
    )

    class Meta:
        verbose_name = "برچسب"
        verbose_name_plural = "برچسب ها"

    # نمایش عنوان برچسب
    def __str__(self):
        return self.title

    # ساخت خودکار اسلاگ از روی عنوان، اگر خالی باشد
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
# ======================================================================================================================
# مدل مقالات وبلاگ
class BlogModels(models.Model):

    # وضعیت انتشار مقاله
    STATUS_CHOICES = (
        ("draft", "پیش نویس"),
        ("published", "منتشر شده"),
    )

    # عنوان مقاله
    title = models.CharField(max_length=255)

    # اسلاگ (آدرس URL مقاله)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True
    )

    # دسته‌بندی مقاله
    category = models.ForeignKey(
        CategoryModels,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blogs"
    )

    # برچسب‌های مقاله (هر مقاله می‌تواند چند برچسب داشته باشد)
    tags = models.ManyToManyField(
        TagModel,
        blank=True,
        related_name="blogs",
        verbose_name="برچسب ها"
    )

    # تصویر شاخص مقاله
    image = models.ImageField(
        upload_to="image/",
        verbose_name="تصویر"
    )

    # توضیح کوتاه مقاله
    short_description = models.TextField(
        verbose_name="خلاصه مقاله"
    )

    # متن کامل مقاله
    content = models.TextField(
        verbose_name="متن مقاله"
    )

    # تعداد بازدید مقاله
    views = models.PositiveIntegerField(
        default=0,
        verbose_name="تعداد بازدید"
    )

    # وضعیت انتشار
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="draft",
        verbose_name="وضعیت"
    )

    # تاریخ ایجاد مقاله
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )

    # تاریخ آخرین ویرایش
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name="آخرین بروزرسانی"
    )

    class Meta:
        # نمایش جدیدترین مقالات در ابتدا
        ordering = ["-created_date"]

        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    # نمایش عنوان مقاله
    def __str__(self):
        return self.title

    # ساخت خودکار اسلاگ از روی عنوان، اگر کاربر خودش وارد نکرده باشد
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
# ======================================================================================================================
# مدل نظرات کاربران روی مقالات
class CommentModel(models.Model):

    # مقاله‌ای که این نظر برای آن ثبت شده است
    blog = models.ForeignKey(
        BlogModels,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="مقاله"
    )

    # نام کامل نویسنده‌ی نظر
    fullname = models.CharField(
        max_length=150,
        verbose_name="نام کامل"
    )

    # ایمیل نویسنده‌ی نظر
    email = models.EmailField(
        verbose_name="ایمیل"
    )

    # وب‌سایت نویسنده‌ی نظر (اختیاری)
    website = models.URLField(
        blank=True,
        null=True,
        verbose_name="وب سایت"
    )

    # متن نظر
    message = models.TextField(
        verbose_name="متن نظر"
    )

    # آیا نظر توسط مدیر تایید شده و قابل نمایش در سایت است؟
    is_approved = models.BooleanField(
        default=False,
        verbose_name="تایید شده"
    )

    # تاریخ ثبت نظر
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ثبت"
    )

    class Meta:
        # نمایش جدیدترین نظرات در ابتدا
        ordering = ["-created_date"]

        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

    # نمایش نام نویسنده و مقاله مرتبط
    def __str__(self):
        return f"{self.fullname} - {self.blog.title}"
# ======================================================================================================================