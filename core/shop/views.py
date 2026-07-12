from django.views.generic import ListView, DetailView
from .models import ProductModels
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

    # فقط محصولات موجود
    def get_queryset(self):
        return ProductModels.objects.filter(
            is_available=True
        )
# ======================================================================================================================
# نمایش جزئیات محصول
class ProductDetailView(DetailView):

    # مدل
    model = ProductModels

    # قالب
    template_name = "shop/shop-detail.html"

    # نام متغیر
    context_object_name = "product"

    # اسلاگ
    slug_field = "slug"
    slug_url_kwarg = "slug"

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
# ======================================================================================================================