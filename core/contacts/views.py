from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from .forms import ContactForm, NewsletterForm
from .models import HistoryItemModel, ProcessStepModel, AwardModel
from team.models import TeamModels
from index.models import GalleryModel
# =====================================================================================================================
# نمایش و پردازش فرم تماس با ما
class ContactView(FormView):

    # قالب صفحه تماس با ما
    template_name = 'contacts/contacts.html'

    # فرم مورد استفاده در این ویو
    form_class = ContactForm

    # مسیر انتقال بعد از ارسال موفق فرم
    success_url = reverse_lazy('contact:contact-us')

    # ذخیره اطلاعات فرم و نمایش پیام موفقیت
    def form_valid(self, form):

        # ذخیره اطلاعات فرم در دیتابیس
        form.save()

        # نمایش پیام موفقیت به کاربر
        messages.success(
            self.request,
            'پیام شما با موفقیت ارسال شد.'
        )

        return super().form_valid(form)
# ======================================================================================================================
# نمایش صفحه‌ی «درباره ما»
class AboutView(TemplateView):

    # قالب صفحه
    template_name = "contacts/about.html"

    # اضافه کردن داده‌های داینامیک صفحه (سابقه، مراحل کاری، جوایز، گالری، نظرات)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # آیتم‌های سابقه/تاریخچه فعال، برای کاروسل «سابقه ما»
        context["history_items"] = HistoryItemModel.objects.filter(is_active=True)

        # مراحل کاری فعال، برای بخش «معماری استثنایی»
        context["process_steps"] = ProcessStepModel.objects.filter(is_active=True)

        # جوایز فعال، برای بخش «جوایز ما در صنعت»
        context["awards"] = AwardModel.objects.filter(is_active=True)

        # تصاویر گالری فعال
        context["about_gallery"] = GalleryModel.objects.filter(is_active=True)

        # اعضای تیمی که مدیر شرکت هستن، برای بخش نظرات
        context["about_managers"] = TeamModels.objects.filter(is_active=True, is_manager=True)

        return context
# ======================================================================================================================
# عضویت کاربر در خبرنامه
class NewsletterSubscribeView(View):

    # پردازش درخواست عضویت در خبرنامه
    def post(self, request, *args, **kwargs):

        # دریافت اطلاعات فرم خبرنامه
        form = NewsletterForm(request.POST)

        # بررسی اعتبار فرم
        if form.is_valid():

            # ذخیره ایمیل کاربر در دیتابیس
            form.save()

            # نمایش پیام موفقیت
            messages.success(
                request,
                "عضویت شما در خبرنامه انجام شد."
            )

        else:

            # نمایش پیام خطا در صورت نامعتبر بودن ایمیل
            messages.error(
                request,
                "ایمیل معتبر وارد کنید یا قبلاً عضو شده‌اید."
            )

        # بازگشت کاربر به صفحه قبلی
        return redirect(request.META.get("HTTP_REFERER", "/"))
# ======================================================================================================================
