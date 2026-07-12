from django.contrib import admin
from .models import ProductModels, CategoryModels
# ======================================================================================================================
# مدیریت دسته‌بندی محصولات
@admin.register(CategoryModels)
class CategoryModelsAdmin(admin.ModelAdmin):

    # ستون‌های قابل نمایش
    list_display = (
        "id",
        "title",
    )

    # جستجو
    search_fields = (
        "title",
    )
# ======================================================================================================================
# مدیریت محصولات
@admin.register(ProductModels)
class ProductModelsAdmin(admin.ModelAdmin):

    # ساخت خودکار اسلاگ
    prepopulated_fields = {
        "slug": ("title",)
    }

    # ستون‌های قابل نمایش
    list_display = (
        "id",
        "title",
        "category",
        "price",
        "is_available",
        "is_featured",
        "views",
        "created_date",
    )

    # فیلترها
    list_filter = (
        "category",
        "is_available",
        "is_featured",
        "created_date",
    )

    # جستجو
    search_fields = (
        "title",
        "description",
    )

    # لینک‌های قابل کلیک
    list_display_links = (
        "id",
        "title",
    )

    # مرتب‌سازی
    ordering = (
        "-created_date",
    )

    # تعداد نمایش در هر صفحه
    list_per_page = 10
# ======================================================================================================================