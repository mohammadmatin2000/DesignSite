from django.contrib import admin
from .models import ServiceModel, ServiceGalleryModel
# ======================================================================================================================
# مدیریت گالری تصاویر خدمت به صورت Inline
class ServiceGalleryInline(admin.TabularInline):
    model = ServiceGalleryModel
    extra = 1
# ======================================================================================================================
# مدیریت خدمات در پنل ادمین (لیست + جزئیات، یک مدل واحد)
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

    # فیلدهای قابل ویرایش مستقیم از لیست
    list_editable = (
        "order",
        "is_active",
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

    # تولید خودکار slug از عنوان
    prepopulated_fields = {
        "slug": ("title",)
    }

    # مرتب‌سازی
    ordering = (
        "order",
    )

    # نمایش گالری تصاویر مربوط به همین خدمت
    inlines = [
        ServiceGalleryInline,
    ]

    # گروه‌بندی فیلدها برای خوانایی بهتر فرم ادمین
    fieldsets = (
        ("اطلاعات اصلی", {
            "fields": ("title", "slug", "image", "order", "is_active")
        }),
        ("نمایش در لیست خدمات", {
            "fields": ("description",)
        }),
        ("صفحه جزئیات", {
            "fields": (
                "about_service",
                "spaces_description",
                "key_elements_description",
            )
        }),
    )
# ======================================================================================================================
