from django.db import models
from shop.models import ProductModels
# ======================================================================================================================
# مدل سبد خرید
class CartModel(models.Model):

    # کاربر صاحب سبد
    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="cart"
    )

    # تاریخ ایجاد
    created_date = models.DateTimeField(auto_now_add=True)

    # آخرین بروزرسانی
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبدهای خرید"

    # جمع کل قیمت سبد
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    # جمع تعداد آیتم‌های سبد
    @property
    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())

    # نمایش عنوان
    def __str__(self):
        return f"سبد خرید {self.user}"
# ======================================================================================================================
# مدل آیتم‌های سبد خرید
class CartItemModel(models.Model):

    # سبد مرتبط
    cart = models.ForeignKey(
        CartModel,
        on_delete=models.CASCADE,
        related_name="items"
    )

    # محصول
    product = models.ForeignKey(
        ProductModels,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    # تعداد
    quantity = models.PositiveIntegerField(default=1)

    # تاریخ اضافه شدن
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("cart", "product")
        ordering = ["-created_date"]
        verbose_name = "آیتم سبد خرید"
        verbose_name_plural = "آیتم های سبد خرید"

    # جمع قیمت این آیتم (قیمت واحد × تعداد)
    @property
    def total_price(self):
        return self.product.price * self.quantity

    # نمایش عنوان
    def __str__(self):
        return f"{self.product.title} × {self.quantity}"
# ======================================================================================================================