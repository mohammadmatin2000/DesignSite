from django.views.generic import ListView, DetailView
from .models import ServiceModel
# ======================================================================================================================
# نمایش لیست خدمات
class ServiceListView(ListView):

    # مدل مورد استفاده
    model = ServiceModel

    # قالب صفحه
    template_name = "services/services.html"

    # نام متغیر ارسالی به قالب
    context_object_name = "services"

    # فقط خدمات فعال، مرتب‌شده بر اساس ترتیب دلخواه
    queryset = ServiceModel.objects.filter(is_active=True).order_by("order")
# ======================================================================================================================
# نمایش جزئیات یک خدمت
class ServiceDetailView(DetailView):

    # مدل مورد استفاده
    model = ServiceModel

    # قالب صفحه
    template_name = "services/service-detail.html"

    # نام متغیر ارسالی به قالب
    context_object_name = "service"

    # فیلد اسلاگ برای پیدا کردن رکورد بر اساس آدرس URL
    slug_field = "slug"
    slug_url_kwarg = "slug"

    # اضافه کردن داده‌های اضافی به قالب (لیست همه‌ی خدمات برای سایدبار)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # همه‌ی خدمات فعال، برای نمایش در سایدبار یا منوی خدمات مشابه
        context["all_services"] = ServiceModel.objects.filter(is_active=True).order_by("order")

        return context
# ======================================================================================================================