from django.contrib import admin
from .models import ProjectCategoryModel, ProjectModel
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
# مدیریت پروژه‌ها در پنل ادمین (لیست + جزئیات، یک مدل واحد)
@admin.register(ProjectModel)
class ProjectAdmin(admin.ModelAdmin):

    # فیلدهای قابل نمایش
    list_display = (
        "id",
        "title",
        "category",
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
        "architect",
    )

    # فیلترها
    list_filter = (
        "category",
        "project_type",
        "year",
        "created_date",
    )

    # پر کردن خودکار slug از روی title
    prepopulated_fields = {
        "slug": ("title",)
    }

    # انتخاب راحت‌تر دسته‌بندی‌های اضافه (چندتایی)
    filter_horizontal = (
        "extra_categories",
    )

    # مرتب‌سازی
    ordering = (
        "-created_date",
    )

    # گروه‌بندی فیلدها در فرم ادمین برای خوانایی بهتر
    fieldsets = (
        ("اطلاعات اصلی", {
            "fields": ("title", "slug", "category", "extra_categories", "image")
        }),
        ("اطلاعات نمایش در لیست", {
            "fields": ("location", "year", "description")
        }),
        ("اطلاعات متا صفحه جزئیات", {
            "fields": (
                "client",
                "project_type",
                "architect",
                "duration",
                "strategy",
                "display_date",
            )
        }),
        ("طراحی با جزئیات", {
            "fields": (
                "short_description",
            )
        }),
        ("ویژگی‌های پروژه - ستون اول", {
            "fields": (
                "feature_one_title", "feature_one_desc",
                "feature_two_title", "feature_two_desc",
                "feature_three_title", "feature_three_desc",
            )
        }),
        ("ویژگی‌های پروژه - ستون دوم", {
            "fields": (
                "feature_four_title", "feature_four_desc",
                "feature_five_title", "feature_five_desc",
            )
        }),
        ("باکس‌های آماری", {
            "fields": (
                ("stat_one_value", "stat_one_label"),
                ("stat_two_value", "stat_two_label"),
                ("stat_three_value", "stat_three_label"),
                ("stat_four_value", "stat_four_label"),
            )
        }),
        ("نتیجه پروژه", {
            "fields": (
                "result_description",
            )
        }),
    )
# ======================================================================================================================