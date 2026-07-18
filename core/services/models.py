from django.db import models
from django.utils.text import slugify
# ======================================================================================================================
# ذخیره خدمات ارائه شده توسط مجموعه (لیست + جزئیات، یک مدل واحد)
class ServiceModel(models.Model):

    # عنوان خدمت
    title = models.CharField(max_length=255)

    # آدرس یکتای صفحه جزئیات
    slug = models.SlugField(unique=True, blank=True, allow_unicode=True)

    # توضیح کوتاه خدمت (کارت لیست)
    description = models.TextField()

    # تصویر شاخص خدمت
    image = models.ImageField(upload_to="images/")

    # -------------------- بخش‌های صفحه جزئیات --------------------

    # بخش "در مورد خدمات"
    about_service = models.TextField(blank=True, verbose_name="در مورد خدمات")

    # بخش "انواع فضاها"
    spaces_description = models.TextField(blank=True, verbose_name="انواع فضاها")

    # بخش "عناصر کلیدی"
    key_elements_description = models.TextField(blank=True, verbose_name="عناصر کلیدی")

    # ترتیب نمایش در سایت
    order = models.PositiveIntegerField(default=0)

    # وضعیت فعال یا غیرفعال بودن خدمت
    is_active = models.BooleanField(default=True)

    # تاریخ ایجاد
    created_date = models.DateTimeField(auto_now_add=True)

    # تاریخ آخرین بروزرسانی
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "خدمت"
        verbose_name_plural = "خدمات"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
# ======================================================================================================================
# ذخیره گالری تصاویر هر خدمت
class ServiceGalleryModel(models.Model):

    service = models.ForeignKey(
        ServiceModel,
        on_delete=models.CASCADE,
        related_name='gallery'
    )

    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.service.title
# ======================================================================================================================