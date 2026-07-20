from django.db import models
from django.utils.text import slugify
# ======================================================================================================================
# مدل دسته‌بندی محصولات
class CategoryModels(models.Model):

    # عنوان دسته‌بندی
    title = models.CharField(max_length=255)

    # آدرس سئو
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True
    )

    class Meta:
        ordering = ["title"]
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    # ساخت خودکار اسلاگ
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                self.title,
                allow_unicode=True
            )
        super().save(*args, **kwargs)

    # نمایش عنوان دسته‌بندی
    def __str__(self):
        return self.title
# ======================================================================================================================
# مدل برچسب محصولات
class TagModels(models.Model):

    # عنوان برچسب
    title = models.CharField(max_length=100)

    # آدرس سئو
    slug = models.SlugField(
        max_length=100,
        unique=True,
        blank=True
    )

    class Meta:
        ordering = ["title"]
        verbose_name = "برچسب"
        verbose_name_plural = "برچسب ها"

    # ساخت خودکار اسلاگ
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                self.title,
                allow_unicode=True
            )
        super().save(*args, **kwargs)

    # نمایش عنوان برچسب
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

    # برچسب‌ها
    tags = models.ManyToManyField(
        TagModels,
        blank=True,
        related_name="products"
    )

    # تصویر شاخص
    image = models.ImageField(
        upload_to="shop/"
    )

    # کد محصول (SKU)
    sku = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        verbose_name="کد محصول (SKU)"
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

    # تعداد موجودی انبار
    stock = models.PositiveIntegerField(default=0)

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

    # درصد تخفیف محاسبه‌شده
    @property
    def discount_percent(self):
        if self.old_price and self.old_price > self.price:
            return round(((self.old_price - self.price) / self.old_price) * 100)
        return 0

    # میانگین امتیاز محصول از نظرات تأییدشده
    @property
    def average_rating(self):
        approved = self.reviews.filter(is_approved=True)
        if not approved.exists():
            return 0
        return round(sum(r.rating for r in approved) / approved.count(), 1)

    # تعداد نظرات تأییدشده
    @property
    def review_count(self):
        return self.reviews.filter(is_approved=True).count()

    # نمایش عنوان محصول
    def __str__(self):
        return self.title
# ======================================================================================================================
# مدل گالری تصاویر محصول
class ProductImageModels(models.Model):

    # محصول مرتبط
    product = models.ForeignKey(
        ProductModels,
        on_delete=models.CASCADE,
        related_name="gallery"
    )

    # تصویر
    image = models.ImageField(
        upload_to="shop/gallery/"
    )

    class Meta:
        verbose_name = "تصویر گالری محصول"
        verbose_name_plural = "گالری تصاویر محصول"

    # نمایش عنوان
    def __str__(self):
        return f"تصویر {self.product.title}"
# ======================================================================================================================
# مدل نظرات محصول
class ProductReviewModels(models.Model):

    RATING_CHOICES = [
        (1, "1 ستاره"),
        (2, "2 ستاره"),
        (3, "3 ستاره"),
        (4, "4 ستاره"),
        (5, "5 ستاره"),
    ]

    # محصول مرتبط
    product = models.ForeignKey(
        ProductModels,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    # نام کامل نظردهنده
    full_name = models.CharField(max_length=255)

    # ایمیل نظردهنده
    email = models.EmailField()

    # امتیاز
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)

    # متن نظر
    comment = models.TextField()

    # تأیید نظر توسط ادمین
    is_approved = models.BooleanField(default=False)

    # تاریخ ثبت
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_date"]
        verbose_name = "نظر محصول"
        verbose_name_plural = "نظرات محصول"

    # نمایش عنوان
    def __str__(self):
        return f"{self.full_name} - {self.product.title}"
# ======================================================================================================================
# مدل علاقه‌مندی‌های کاربر (Wishlist)
class WishlistModel(models.Model):

    # کاربر
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="wishlist_items"
    )

    # محصول
    product = models.ForeignKey(
        ProductModels,
        on_delete=models.CASCADE,
        related_name="wishlisted_by"
    )

    # تاریخ اضافه شدن
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")
        ordering = ["-created_date"]
        verbose_name = "علاقه‌مندی"
        verbose_name_plural = "علاقه‌مندی‌ها"

    def __str__(self):
        return f"{self.user} - {self.product.title}"
# ======================================================================================================================