from django.views.generic.base import TemplateView
# ======================================================================================================================
# نمایش صفحه اصلی سایت
class IndexView(TemplateView):

    template_name = "index/index.html"

    context_object_name = "index"
# ======================================================================================================================