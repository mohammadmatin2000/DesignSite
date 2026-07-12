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
# ======================================================================================================================