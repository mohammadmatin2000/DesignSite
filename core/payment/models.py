from django.db import models
from order.models import OrderModel
# ======================================================================================================================
# مدل تراکنش پرداخت
class PaymentModel(models.Model):

    STATUS_CHOICES = [
        ("pending", "در انتظار پرداخت"),
        ("success", "موفق"),
        ("failed", "ناموفق"),
    ]

    # سفارش مرتبط
    order = models.ForeignKey(
        OrderModel,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    # مبلغ پرداخت (تومان)
    amount = models.PositiveIntegerField()

    # کد Authority دریافتی از زرین‌پال
    authority = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # کد پیگیری (RefID) در صورت موفقیت
    ref_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # وضعیت پرداخت
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    # تاریخ ایجاد تراکنش
    created_date = models.DateTimeField(auto_now_add=True)

    # آخرین بروزرسانی
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_date"]
        verbose_name = "تراکنش پرداخت"
        verbose_name_plural = "تراکنش های پرداخت"

    # نمایش عنوان
    def __str__(self):
        return f"پرداخت سفارش #{self.order.id} - {self.get_status_display()}"
# ======================================================================================================================