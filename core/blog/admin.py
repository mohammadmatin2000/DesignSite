from django.contrib import admin
from .models import BlogModels, CategoryModels
# ======================================================================================================================
# مدیریت دسته‌بندی مقالات
@admin.register(CategoryModels)
class CategoryModelsAdmin(admin.ModelAdmin):

    # نمایش ستون‌ها
    list_display = ("id", "title")

    # جستجو بر اساس عنوان
    search_fields = ("title",)
# ======================================================================================================================
# مدیریت مقالات
@admin.register(BlogModels)
class BlogModelsAdmin(admin.ModelAdmin):

    # ساخت خودکار اسلاگ از عنوان
    prepopulated_fields = {"slug": ("title",)}

    # ستون‌های قابل نمایش
    list_display = (
        "id",
        "title",
        "category",
        "status",
        "views",
        "created_date",
    )

    # فیلترها
    list_filter = (
        "status",
        "category",
        "created_date",
    )

    # جستجو
    search_fields = (
        "title",
        "short_description",
        "content",
    )

    # لینک قابل کلیک
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