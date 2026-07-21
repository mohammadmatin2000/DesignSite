from django.contrib import admin
from .models import CartModel, CartItemModel
# ======================================================================================================================
# نمایش آیتم‌های سبد به صورت اینلاین داخل سبد خرید
class CartItemInline(admin.TabularInline):
    model = CartItemModel
    extra = 0
    readonly_fields = ("total_price",)
    fields = ("product", "quantity", "total_price")
# ======================================================================================================================
# مدیریت سبد خرید
@admin.register(CartModel)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ("user", "total_quantity", "total_price", "updated_date")
    search_fields = ("user__username", "user__email")
    readonly_fields = ("total_price", "total_quantity")
    inlines = [CartItemInline]
# ======================================================================================================================