from django.contrib import admin
from .models import (
    CategoryModels,
    TagModels,
    ProductModels,
    ProductImageModels,
    ProductReviewModels,
    WishlistModel
)
# ======================================================================================================================
# نمایش inline گالری تصاویر داخل صفحه محصول
class ProductImageInline(admin.TabularInline):
    model = ProductImageModels
    extra = 1
# ======================================================================================================================
# نمایش inline نظرات داخل صفحه محصول
class ProductReviewInline(admin.TabularInline):
    model = ProductReviewModels
    extra = 0
    fields = ("full_name", "email", "rating", "comment", "is_approved", "created_date")
    readonly_fields = ("created_date",)
# ======================================================================================================================
# ادمین دسته‌بندی
@admin.register(CategoryModels)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
# ======================================================================================================================
# ادمین برچسب
@admin.register(TagModels)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}
# ======================================================================================================================
# ادمین محصول
@admin.register(ProductModels)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "price",
        "old_price",
        "stock",
        "is_available",
        "is_featured",
        "views",
        "created_date",
    )
    list_filter = ("category", "tags", "is_available", "is_featured", "created_date")
    search_fields = ("title", "sku", "short_description", "description")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    readonly_fields = ("views", "created_date", "updated_date")
    inlines = [ProductImageInline, ProductReviewInline]

    fieldsets = (
        ("اطلاعات اصلی", {
            "fields": ("title", "slug", "category", "tags", "image", "sku")
        }),
        ("قیمت و موجودی", {
            "fields": ("price", "old_price", "stock", "is_available", "is_featured")
        }),
        ("توضیحات", {
            "fields": ("short_description", "description")
        }),
        ("اطلاعات سیستمی", {
            "fields": ("views", "created_date", "updated_date")
        }),
    )
# ======================================================================================================================
# ادمین نظرات محصول (نمای مستقل برای مدیریت سریع تأیید نظرات)
@admin.register(ProductReviewModels)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ("full_name", "product", "rating", "is_approved", "created_date")
    list_filter = ("is_approved", "rating", "created_date")
    search_fields = ("full_name", "email", "comment", "product__title")
    actions = ["approve_reviews", "unapprove_reviews"]

    # تأیید گروهی نظرات انتخاب‌شده
    @admin.action(description="تأیید نظرات انتخاب‌شده")
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)

    # لغو تأیید گروهی نظرات انتخاب‌شده
    @admin.action(description="لغو تأیید نظرات انتخاب‌شده")
    def unapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)
# ======================================================================================================================
#برای علاقه مندی
@admin.register(WishlistModel)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "created_date")
    search_fields = ("user__username", "product__title")
    list_filter = ("created_date",)
# ======================================================================================================================