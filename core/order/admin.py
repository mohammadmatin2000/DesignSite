from django.contrib import admin
from .models import OrderModel, OrderItemModel
# ======================================================================================================================
# نمایش آیتم‌های سفارش به صورت اینلاین
class OrderItemInline(admin.TabularInline):
    model = OrderItemModel
    extra = 0
    readonly_fields = ("product", "product_title", "price", "quantity", "total_price")
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False
# ======================================================================================================================
# مدیریت سفارش‌ها
@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "full_name", "status", "total_price", "created_date")
    list_filter = ("status", "created_date")
    search_fields = ("full_name", "phone", "user__username", "user__email")
    readonly_fields = ("user", "total_price", "total_quantity", "created_date", "updated_date")
    list_editable = ("status",)
    inlines = [OrderItemInline]

    fieldsets = (
        ("اطلاعات کاربر", {"fields": ("user",)}),
        ("اطلاعات گیرنده", {"fields": ("full_name", "phone", "address", "postal_code", "note")}),
        ("وضعیت سفارش", {"fields": ("status", "total_price", "total_quantity")}),
        ("تاریخ‌ها", {"fields": ("created_date", "updated_date")}),
    )
# ======================================================================================================================