from django.contrib import admin
from .models import GalleryModel
# ======================================================================================================================
# مدیریت تصاویر گالری
@admin.register(GalleryModel)
class GalleryModelAdmin(admin.ModelAdmin):

    # ستون‌های قابل نمایش
    list_display = ("id", "alt_text", "order", "is_active")

    # امکان ویرایش مستقیم ترتیب و وضعیت نمایش از داخل لیست
    list_editable = ("order", "is_active")

    # فیلترها
    list_filter = ("is_active",)
# ======================================================================================================================