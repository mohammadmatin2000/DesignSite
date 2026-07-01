from django.views.generic import ListView, DetailView
from .models import ServiceModel, ServiceDetailModel
# ======================================================================================================================
# نمایش لیست خدمات
class ServiceListView(ListView):

    # مدل مرتبط
    model = ServiceModel

    # قالب صفحه
    template_name = "services/services.html"

    # نام متغیر ارسالی به قالب
    context_object_name = "services"

    # فقط خدمات فعال نمایش داده شوند
    queryset = ServiceModel.objects.filter(
        is_active=True
    ).order_by("order")
# ======================================================================================================================
# نمایش جزئیات هر خدمت
class ServiceDetailView(DetailView):

    # مدل مرتبط
    model = ServiceDetailModel

    # قالب صفحه
    template_name = "services/service-detail.html"

    # نام متغیر ارسالی به قالب
    context_object_name = "service"

    # استفاده از slug
    slug_field = "slug"
    slug_url_kwarg = "slug"
# ======================================================================================================================