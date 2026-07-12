from django.views.generic import ListView, DetailView
from .models import BlogModels
# ======================================================================================================================
# نمایش لیست مقالات
class BlogListView(ListView):

    # مدل مورد استفاده
    model = BlogModels

    # قالب صفحه
    template_name = "blog/blog-list.html"

    # نام متغیر ارسالی به قالب
    context_object_name = "blogs"

    # تعداد مقالات در هر صفحه
    paginate_by = 6

    # فقط مقالات منتشر شده
    def get_queryset(self):
        return BlogModels.objects.filter(status="published")
# ======================================================================================================================
# نمایش جزئیات مقاله
class BlogDetailView(DetailView):

    # مدل مورد استفاده
    model = BlogModels

    # قالب صفحه
    template_name = "blog/blog-detail.html"

    # نام متغیر ارسالی به قالب
    context_object_name = "blog_detail"

    # پیدا کردن مقاله بر اساس اسلاگ
    slug_field = "slug"
    slug_url_kwarg = "slug"

    # فقط مقالات منتشر شده
    def get_queryset(self):
        return BlogModels.objects.filter(status="published")
# ======================================================================================================================