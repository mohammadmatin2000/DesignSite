from django.urls import path
from .views import BlogListView, BlogDetailView
# ======================================================================================================================
app_name = "blog"
urlpatterns = [

    # صفحه لیست مقالات
    path(
        "blog_list/",
        BlogListView.as_view(),
        name="blog_list"
    ),

    # صفحه جزئیات مقاله
    path(
        "blog_detail/<slug:slug>/",
        BlogDetailView.as_view(),
        name="blog_detail"
    ),

]
# ======================================================================================================================