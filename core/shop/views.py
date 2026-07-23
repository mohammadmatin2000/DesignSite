from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.urls import reverse
from .models import ProductModels, CategoryModels, TagModels,WishlistModel
from .forms import ProductReviewForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
# ======================================================================================================================
# نمایش لیست محصولات
class ProductListView(ListView):

    # مدل
    model = ProductModels

    # قالب
    template_name = "shop/shop.html"

    # نام متغیر در قالب
    context_object_name = "products"

    # تعداد محصولات در هر صفحه
    paginate_by = 9

    # فقط محصولات موجود + اعمال فیلترها
    def get_queryset(self):
        queryset = ProductModels.objects.filter(is_available=True)

        # فیلتر بر اساس دسته‌بندی (پشتیبانی از چند دسته هم‌زمان)
        categories = self.request.GET.getlist("categories")
        if categories:
            queryset = queryset.filter(category__slug__in=categories)

        # فیلتر بر اساس برچسب
        tag = self.request.GET.get("tag")
        if tag:
            queryset = queryset.filter(tags__slug=tag)

        # جستجو در عنوان و توضیح کوتاه
        search_query = self.request.GET.get("q")
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)

        # فیلتر بازه قیمت
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # مرتب‌سازی
        sort = self.request.GET.get("sort")
        sort_map = {
            "popular": "-views",
            "date": "-created_date",
            "price_low": "price",
            "price_high": "-price",
            "featured": "-is_featured",
        }
        if sort in sort_map:
            queryset = queryset.order_by(sort_map[sort])

        return queryset.distinct()

    # اطلاعات تکمیلی برای سایدبار (دسته‌بندی‌ها، محصولات محبوب)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = CategoryModels.objects.all()
        context["tags"] = TagModels.objects.all()

        # ویجت محصولات محبوب برای سایدبار
        context["popular_products"] = ProductModels.objects.filter(
            is_available=True
        ).order_by("-views")[:4]

        # حفظ مقادیر فیلتر فعلی برای نمایش در فرم
        context["selected_categories"] = self.request.GET.getlist("categories")
        context["current_search"] = self.request.GET.get("q", "")
        context["current_sort"] = self.request.GET.get("sort", "")

        return context
# ======================================================================================================================
# نمایش جزئیات محصول
class ProductDetailView(FormMixin, DetailView):

    # مدل
    model = ProductModels

    # قالب
    template_name = "shop/shop-detail.html"

    # نام متغیر
    context_object_name = "product"

    # اسلاگ
    slug_field = "slug"
    slug_url_kwarg = "slug"

    # فرم ثبت نظر
    form_class = ProductReviewForm

    # فقط محصولات موجود
    def get_queryset(self):
        return ProductModels.objects.filter(
            is_available=True
        )

    # افزایش تعداد بازدید
    def get_object(self, queryset=None):

        obj = super().get_object(queryset)

        obj.views += 1
        obj.save(update_fields=["views"])

        return obj

    # اطلاعات تکمیلی: محصولات مرتبط + نظرات تأییدشده
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product = self.object

        # محصولات مرتبط از همون دسته‌بندی
        context["related_products"] = ProductModels.objects.filter(
            is_available=True,
            category=product.category
        ).exclude(id=product.id)[:4]

        # نظرات تأییدشده
        context["reviews"] = product.reviews.filter(is_approved=True)

        if "form" not in kwargs:
            context["form"] = self.get_form()

        return context

    # مسیر بازگشت بعد از ثبت موفق نظر
    def get_success_url(self):
        return reverse("shop:shop-detail", kwargs={"slug": self.object.slug})

    # ثبت نظر جدید
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        review = form.save(commit=False)
        review.product = self.object
        review.save()

        messages.success(
            self.request,
            "نظر شما با موفقیت ثبت شد و پس از تأیید نمایش داده می‌شود."
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return self.render_to_response(context)
# ======================================================================================================================
# تاگل کردن علاقه‌مندی (افزودن/حذف) - نیازمند لاگین
class WishlistToggleView(LoginRequiredMixin, View):

    login_url = "accounts:login"

    def post(self, request, slug, *args, **kwargs):
        product = get_object_or_404(ProductModels, slug=slug)

        wishlist_item, created = WishlistModel.objects.get_or_create(
            user=request.user,
            product=product
        )

        if not created:
            wishlist_item.delete()
            is_wishlisted = False
        else:
            is_wishlisted = True

        # اگه درخواست AJAX بود، JSON برگردون
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"is_wishlisted": is_wishlisted})

        return redirect(request.META.get("HTTP_REFERER", "/"))
# ======================================================================================================================