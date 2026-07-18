from django.db import models
# ======================================================================================================================
# مدل تصاویر گالری (برای نمایش در صفحه‌ی اصلی)
class GalleryModel(models.Model):

    # تصویر
    image = models.ImageField(
        upload_to="image/gallery/",
        verbose_name="تصویر"
    )

    # متن جایگزین تصویر (برای دسترسی‌پذیری و سئو)
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="متن جایگزین"
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

    # تاریخ ایجاد
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    updated_date = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["order", "-created_date"]
        verbose_name = "تصویر گالری"
        verbose_name_plural = "گالری تصاویر"

    def __str__(self):
        return self.alt_text or f"تصویر گالری #{self.pk}"
# ======================================================================================================================