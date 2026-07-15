from django.contrib import admin
from .models import BlogModels, CategoryModels, TagModel, CommentModel
# ======================================================================================================================
# مدیریت دسته‌بندی مقالات
@admin.register(CategoryModels)
class CategoryModelsAdmin(admin.ModelAdmin):

    # نمایش ستون‌ها
    list_display = ("id", "title")

    # جستجو بر اساس عنوان
    search_fields = ("title",)
# ======================================================================================================================
# مدیریت برچسب‌های مقالات
@admin.register(TagModel)
class TagModelAdmin(admin.ModelAdmin):

    # ساخت خودکار اسلاگ از عنوان
    prepopulated_fields = {"slug": ("title",)}

    # ستون‌های قابل نمایش
    list_display = ("id", "title", "slug")

    # جستجو بر اساس عنوان
    search_fields = ("title",)
# ======================================================================================================================
# مدیریت مقالات
@admin.register(BlogModels)
class BlogModelsAdmin(admin.ModelAdmin):

    # ساخت خودکار اسلاگ از عنوان
    prepopulated_fields = {"slug": ("title",)}

    # انتخاب راحت‌تر برچسب‌ها (باکس دوطرفه به‌جای لیست کشویی چندتایی)
    filter_horizontal = ("tags",)

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
# مدیریت نظرات کاربران روی مقالات
@admin.register(CommentModel)
class CommentModelAdmin(admin.ModelAdmin):

    # ستون‌های قابل نمایش
    list_display = (
        "id",
        "fullname",
        "email",
        "blog",
        "is_approved",
        "created_date",
    )

    # فیلترها (سریع پیدا کردن نظرات تایید نشده)
    list_filter = (
        "is_approved",
        "created_date",
    )

    # جستجو
    search_fields = (
        "fullname",
        "email",
        "message",
    )

    # لینک قابل کلیک
    list_display_links = (
        "id",
        "fullname",
    )

    # مرتب‌سازی (جدیدترین نظرات اول، برای بررسی سریع‌تر)
    ordering = (
        "-created_date",
    )

    # تعداد نمایش در هر صفحه
    list_per_page = 20

    # امکان تایید یا رد گروهی چند نظر همزمان
    actions = ["approve_comments", "disapprove_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "تایید نظرات انتخاب شده"

    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_comments.short_description = "لغو تایید نظرات انتخاب شده"
# ======================================================================================================================