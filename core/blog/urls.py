from django.urls import path
from .views import BlogListView, BlogDetailView
# ======================================================================================================================
app_name = "blog"
urlpatterns = [

    # صفحه لیست مقالات
    path(
        "blog-list/",
        BlogListView.as_view(),
        name="blog-list"
    ),

    # صفحه جزئیات مقاله
    path(
        "blog-detail/<slug:slug>/",
        BlogDetailView.as_view(),
        name="blog-detail"
    ),

]
# ======================================================================================================================