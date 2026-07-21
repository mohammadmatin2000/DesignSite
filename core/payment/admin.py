from django.contrib import admin
from .models import PaymentModel
# ======================================================================================================================
# مدیریت تراکنش‌های پرداخت
@admin.register(PaymentModel)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "amount", "status", "ref_id", "created_date")
    list_filter = ("status", "created_date")
    search_fields = ("order__id", "authority", "ref_id", "order__user__username")
    readonly_fields = ("order", "amount", "authority", "ref_id", "status", "created_date", "updated_date")

    def has_add_permission(self, request):
        return False
# ======================================================================================================================