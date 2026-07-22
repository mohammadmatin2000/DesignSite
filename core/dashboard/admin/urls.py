from django.urls import path
from . import views
# ======================================================================================================================
app_name = "admin"
# ======================================================================================================================
urlpatterns = [
    # صفحه اصلی
    path("home/", views.AdminHomeView.as_view(), name="home"),

    # سفارش‌ها
    path("order/", views.AdminOrderListView.as_view(), name="order-list"),
    path("order/<int:pk>/", views.AdminOrderDetailView.as_view(), name="order-detail"),
    path("order/<int:pk>/update-status/", views.AdminOrderUpdateStatusView.as_view(), name="order-update-status"),

    # پیام‌ها
    path("messages/", views.AdminMessageListView.as_view(), name="message-list"),
    path("messages/<int:pk>/", views.AdminMessageDetailView.as_view(), name="message-detail"),
    path("messages/<int:pk>/delete/", views.AdminMessageDeleteView.as_view(), name="message-delete"),

    # محصولات
    path("products/", views.AdminProductListView.as_view(), name="product-list"),
    path("products/create/", views.AdminProductCreateView.as_view(), name="product-create"),
    path("products/<int:pk>/update/", views.AdminProductUpdateView.as_view(), name="product-update"),
    path("products/<int:pk>/delete/", views.AdminProductDeleteView.as_view(), name="product-delete"),

    # دسته‌بندی و برچسب شاپ
    path("categories/", views.AdminCategoryListView.as_view(), name="category-list"),
    path("categories/create/", views.AdminCategoryCreateView.as_view(), name="category-create"),
    path("categories/<int:pk>/update/", views.AdminCategoryUpdateView.as_view(), name="category-update"),
    path("categories/<int:pk>/delete/", views.AdminCategoryDeleteView.as_view(), name="category-delete"),

    path("tags/", views.AdminTagListView.as_view(), name="tag-list"),
    path("tags/create/", views.AdminTagCreateView.as_view(), name="tag-create"),
    path("tags/<int:pk>/update/", views.AdminTagUpdateView.as_view(), name="tag-update"),
    path("tags/<int:pk>/delete/", views.AdminTagDeleteView.as_view(), name="tag-delete"),

    # خدمات
    path("services/", views.AdminServiceListView.as_view(), name="service-list"),
    path("services/create/", views.AdminServiceCreateView.as_view(), name="service-create"),
    path("services/<int:pk>/update/", views.AdminServiceUpdateView.as_view(), name="service-update"),
    path("services/<int:pk>/delete/", views.AdminServiceDeleteView.as_view(), name="service-delete"),
    path("services/gallery/create/", views.AdminServiceGalleryCreateView.as_view(), name="service-gallery-create"),
    path("services/gallery/<int:pk>/delete/", views.AdminServiceGalleryDeleteView.as_view(), name="service-gallery-delete"),

    # تیم
    path("team/", views.AdminTeamListView.as_view(), name="team-list"),
    path("team/create/", views.AdminTeamCreateView.as_view(), name="team-create"),
    path("team/<int:pk>/update/", views.AdminTeamUpdateView.as_view(), name="team-update"),
    path("team/<int:pk>/delete/", views.AdminTeamDeleteView.as_view(), name="team-delete"),

    # گالری صفحه اصلی
    path("gallery/", views.AdminGalleryListView.as_view(), name="gallery-list"),
    path("gallery/create/", views.AdminGalleryCreateView.as_view(), name="gallery-create"),
    path("gallery/<int:pk>/update/", views.AdminGalleryUpdateView.as_view(), name="gallery-update"),
    path("gallery/<int:pk>/delete/", views.AdminGalleryDeleteView.as_view(), name="gallery-delete"),

    # بلاگ
    path("blog/", views.AdminBlogListView.as_view(), name="blog-list"),
    path("blog/create/", views.AdminBlogCreateView.as_view(), name="blog-create"),
    path("blog/<int:pk>/update/", views.AdminBlogUpdateView.as_view(), name="blog-update"),
    path("blog/<int:pk>/delete/", views.AdminBlogDeleteView.as_view(), name="blog-delete"),

    # دسته‌بندی و برچسب بلاگ
    path("blog/categories/", views.AdminBlogCategoryListView.as_view(), name="blog-category-list"),
    path("blog/categories/create/", views.AdminBlogCategoryCreateView.as_view(), name="blog-category-create"),
    path("blog/categories/<int:pk>/update/", views.AdminBlogCategoryUpdateView.as_view(), name="blog-category-update"),
    path("blog/categories/<int:pk>/delete/", views.AdminBlogCategoryDeleteView.as_view(), name="blog-category-delete"),

    path("blog/tags/", views.AdminBlogTagListView.as_view(), name="blog-tag-list"),
    path("blog/tags/create/", views.AdminBlogTagCreateView.as_view(), name="blog-tag-create"),
    path("blog/tags/<int:pk>/update/", views.AdminBlogTagUpdateView.as_view(), name="blog-tag-update"),
    path("blog/tags/<int:pk>/delete/", views.AdminBlogTagDeleteView.as_view(), name="blog-tag-delete"),

    # نظرات بلاگ
    path("comments/", views.AdminCommentListView.as_view(), name="comment-list"),
    path("comments/<int:pk>/approve/", views.AdminCommentApproveView.as_view(), name="comment-approve"),
    path("comments/<int:pk>/delete/", views.AdminCommentDeleteView.as_view(), name="comment-delete"),
]
# ======================================================================================================================