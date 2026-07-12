from django.db import models
from django.utils.text import slugify
# ======================================================================================================================
# مدل دسته‌بندی محصولات
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
# مدل محصولات
class ProductModels(models.Model):

    # عنوان محصول
    title = models.CharField(max_length=255)

    # آدرس سئو
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True
    )

    # دسته‌بندی
    category = models.ForeignKey(
        CategoryModels,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products"
    )

    # تصویر شاخص
    image = models.ImageField(
        upload_to="shop/"
    )

    # قیمت
    price = models.PositiveIntegerField()

    # قیمت قبل از تخفیف
    old_price = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    # توضیح کوتاه
    short_description = models.TextField()

    # توضیحات کامل
    description = models.TextField()

    # موجود بودن
    is_available = models.BooleanField(default=True)

    # محصول ویژه
    is_featured = models.BooleanField(default=False)

    # تعداد بازدید
    views = models.PositiveIntegerField(default=0)

    # تاریخ ایجاد
    created_date = models.DateTimeField(auto_now_add=True)

    # آخرین بروزرسانی
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    # ساخت خودکار اسلاگ
    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(
                self.title,
                allow_unicode=True
            )

        super().save(*args, **kwargs)

    # نمایش عنوان محصول
    def __str__(self):
        return self.title
# ======================================================================================================================