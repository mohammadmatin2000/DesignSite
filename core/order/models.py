from django.db import models
from shop.models import ProductModels
# ======================================================================================================================
# مدل سفارش
class OrderModel(models.Model):

    STATUS_CHOICES = [
        ("pending", "در انتظار پرداخت"),
        ("paid", "پرداخت شده"),
        ("shipped", "ارسال شده"),
        ("delivered", "تحویل داده شده"),
        ("canceled", "لغو شده"),
    ]

    # کاربر ثبت‌کننده سفارش
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="order"
    )

    # نام کامل گیرنده
    full_name = models.CharField(max_length=255)

    # شماره تماس گیرنده
    phone = models.CharField(max_length=20)

    # آدرس کامل ارسال
    address = models.TextField()

    # کد پستی
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    # یادداشت مشتری (اختیاری)
    note = models.TextField(
        blank=True,
        null=True
    )

    # وضعیت سفارش
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    # تاریخ ثبت سفارش
    created_date = models.DateTimeField(auto_now_add=True)

    # آخرین بروزرسانی
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش ها"

    # جمع کل قیمت سفارش
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    # جمع تعداد کالاهای سفارش
    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    # نمایش عنوان
    def __str__(self):
        return f"سفارش #{self.id} - {self.user}"
# ======================================================================================================================
# مدل آیتم‌های سفارش
class OrderItemModel(models.Model):

    # سفارش مرتبط
    order = models.ForeignKey(
        OrderModel,
        on_delete=models.CASCADE,
        related_name="items"
    )

    # محصول (در صورت حذف محصول، آیتم سفارش باقی می‌ماند)
    product = models.ForeignKey(
        ProductModels,
        on_delete=models.SET_NULL,
        null=True,
        related_name="order_items"
    )

    # عنوان محصول در لحظه خرید (اسنپ‌شات، مستقل از تغییرات بعدی محصول)
    product_title = models.CharField(max_length=255)

    # قیمت واحد در لحظه خرید (اسنپ‌شات)
    price = models.PositiveIntegerField()

    # تعداد
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم های سفارش"

    # جمع قیمت این آیتم
    @property
    def total_price(self):
        return self.price * self.quantity

    # نمایش عنوان
    def __str__(self):
        return f"{self.product_title} × {self.quantity}"
# ======================================================================================================================