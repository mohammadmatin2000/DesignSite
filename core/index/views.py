from django.views.generic import TemplateView
from .models import GalleryModel
from services.models import ServiceModel
from blog.models import BlogModels
from team.models import TeamModels
# ======================================================================================================================
# نمایش صفحه‌ی اصلی سایت
class IndexView(TemplateView):

    # قالب صفحه
    template_name = "index/index.html"

    # اضافه کردن داده‌های داینامیک صفحه اصلی (خدمات، مدیران، وبلاگ، گالری)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # خدمات فعال، برای نمایش در کاروسل خدمات
        context["home_services"] = ServiceModel.objects.filter(is_active=True).order_by("order")[:3]

        # اعضای تیمی که مدیر شرکت هستن، برای بخش نظرات
        context["home_managers"] = TeamModels.objects.filter(is_active=True, is_manager=True)

        # آخرین مقالات منتشرشده، برای بخش وبلاگ
        context["home_blogs"] = BlogModels.objects.filter(status="published").order_by("-created_date")[:3]

        # تصاویر گالری فعال، برای نمایش در کاروسل صفحه اصلی
        context["home_gallery"] = GalleryModel.objects.filter(is_active=True)

        return context
# ======================================================================================================================