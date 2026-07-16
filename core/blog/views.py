from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.db.models import Q
from django.urls import reverse
from .models import BlogModels, CategoryModels, TagModel
from .forms import CommentForm
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

    # فقط مقالات منتشر شده + پشتیبانی از جستجو
    def get_queryset(self):
        queryset = BlogModels.objects.filter(status="published")

        # دریافت عبارت جستجو از پارامتر q در URL
        query = self.request.GET.get("q")

        # دریافت پارامتر دسته‌بندی
        category_id = self.request.GET.get("category")

        # دریافت پارامتر برچسب
        tag_slug = self.request.GET.get("tag")

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(short_description__icontains=query) |
                Q(content__icontains=query)
            )

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)

        return queryset

    # اضافه کردن داده‌های اضافی به قالب (دسته‌بندی‌ها، عبارت جستجو، پست‌های اخیر، برچسب‌ها)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # ارسال دسته‌بندی‌ها به سایدبار
        context["categories"] = CategoryModels.objects.all()

        # حفظ عبارت جستجو در اینپوت بعد از ارسال فرم
        context["query"] = self.request.GET.get("q", "")

        # پنج پست اخیر برای سایدبار
        context["recent_posts"] = BlogModels.objects.filter(
            status="published"
        ).order_by("-created_date")[:4]

        # همه‌ی برچسب‌های موجود برای سایدبار
        context["all_tags"] = TagModel.objects.all()

        return context
# ======================================================================================================================
# نمایش جزئیات یک مقاله + دریافت و ثبت نظر کاربران
class BlogDetailView(FormMixin, DetailView):

    model = BlogModels
    template_name = "blog/blog-detail.html"
    context_object_name = "blog"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    # فرم مورد استفاده برای ثبت نظر
    form_class = CommentForm

    # فقط مقالات منتشر شده قابل مشاهده باشند
    def get_queryset(self):
        return BlogModels.objects.filter(status="published")

    # افزایش تعداد بازدید هر بار که صفحه باز میشه
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save(update_fields=["views"])
        return obj

    # آدرس بازگشت بعد از ثبت موفق نظر (همان صفحه‌ی مقاله)
    def get_success_url(self):
        return reverse("blog:blog-detail", kwargs={"slug": self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = CategoryModels.objects.all()

        context["recent_posts"] = BlogModels.objects.filter(
            status="published"
        ).order_by("-created_date")[:4]

        # فقط نظرات تایید شده به کاربر نمایش داده شود
        context["comments"] = self.object.comments.filter(is_approved=True)

        # همه‌ی برچسب‌های موجود برای سایدبار
        context["all_tags"] = TagModel.objects.all()

        # اگر فرم از قبل در context نیامده (مثلاً در حالت GET) بسازش
        if "form" not in kwargs:
            context["form"] = self.get_form()

        return context

    # مدیریت درخواست POST (زمانی که کاربر فرم نظر را ارسال می‌کند)
    def post(self, request, *args, **kwargs):
        # چون در DetailView معمولی self.object در post تنظیم نمی‌شود، خودمان تنظیمش می‌کنیم
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # وقتی فرم معتبر است، نظر را با اتصال به مقاله‌ی جاری ذخیره کن
    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.blog = self.object
        comment.save()
        return super().form_valid(form)

    # اگر فرم نامعتبر بود، همان صفحه را با خطاها دوباره نمایش بده
    def form_invalid(self, form):
        print(form.errors)
        context = self.get_context_data(form=form)
        return self.render_to_response(context)
# ======================================================================================================================