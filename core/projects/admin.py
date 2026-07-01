from django.contrib import admin
from .models import (
    ProjectCategoryModel,
    ProjectModel,
    ProjectDetailModels,
)
# ======================================================================================================================
# مدیریت دسته‌بندی پروژه‌ها در پنل ادمین
@admin.register(ProjectCategoryModel)
class ProjectCategoryAdmin(admin.ModelAdmin):

    # فیلدهای قابل نمایش
    list_display = (
        "id",
        "title",
    )

    # فیلدهای قابل جستجو
    search_fields = (
        "title",
    )
# ======================================================================================================================
# مدیریت پروژه‌ها در پنل ادمین
@admin.register(ProjectModel)
class ProjectAdmin(admin.ModelAdmin):

    # فیلدهای قابل نمایش
    list_display = (
        "id",
        "title",
        "category",
        "location",
        "year",
        "created_date",
    )

    # فیلدهای قابل جستجو
    search_fields = (
        "title",
        "location",
    )

    # فیلترها
    list_filter = (
        "category",
        "year",
        "created_date",
    )

    # مرتب‌سازی
    ordering = (
        "-created_date",
    )
# ======================================================================================================================
# مدیریت جزئیات پروژه‌ها در پنل ادمین
@admin.register(ProjectDetailModels)
class ProjectDetailAdmin(admin.ModelAdmin):

    # فیلدهای قابل نمایش
    list_display = (
        "id",
        "title",
        "client",
        "project_type",
        "location",
        "year",
        "created_date",
    )

    # فیلدهای قابل جستجو
    search_fields = (
        "title",
        "client",
        "location",
    )

    # فیلترها
    list_filter = (
        "project_type",
        "year",
        "created_date",
    )

    # پر کردن خودکار slug از روی title
    prepopulated_fields = {
        "slug": ("title",)
    }

    # مرتب‌سازی
    ordering = (
        "-created_date",
    )
# ======================================================================================================================