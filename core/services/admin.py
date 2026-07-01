from django.contrib import admin
from .models import (
    ServiceModel,
    ServiceDetailModel,
    ServiceGalleryModel,
)
# ======================================================================================================================
# مدیریت گالری تصاویر خدمت به صورت Inline
class ServiceGalleryInline(admin.TabularInline):
    model = ServiceGalleryModel
    extra = 1
# ======================================================================================================================
# مدیریت جزئیات خدمات در پنل ادمین
@admin.register(ServiceDetailModel)
class ServiceDetailAdmin(admin.ModelAdmin):

    # فیلدهای قابل نمایش
    list_display = (
        "id",
        "title",
        "service",
        "created_date",
    )

    # فیلدهای قابل جستجو
    search_fields = (
        "title",
        "service__title",
    )

    # مرتب‌سازی
    ordering = (
        "-created_date",
    )

    # تولید خودکار slug از عنوان
    prepopulated_fields = {
        "slug": ("title",)
    }

    # نمایش گالری تصاویر در صفحه جزئیات
    inlines = [
        ServiceGalleryInline,
    ]
# ======================================================================================================================
# مدیریت خدمات در پنل ادمین
@admin.register(ServiceModel)
class ServiceAdmin(admin.ModelAdmin):

    # فیلدهای قابل نمایش
    list_display = (
        "id",
        "title",
        "order",
        "is_active",
        "created_date",
    )

    # فیلدهای قابل جستجو
    search_fields = (
        "title",
    )

    # فیلترها
    list_filter = (
        "is_active",
        "created_date",
    )

    # مرتب‌سازی
    ordering = (
        "order",
    )
# ======================================================================================================================
# ثبت گالری تصاویر
@admin.register(ServiceGalleryModel)
class ServiceGalleryAdmin(admin.ModelAdmin):

    # فیلدهای قابل نمایش
    list_display = (
        "id",
        "service",
    )

    # فیلدهای قابل جستجو
    search_fields = (
        "service__title",
    )
# ======================================================================================================================