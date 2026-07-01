from django.views.generic.edit import FormView
from django.views import View
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from .forms import ContactForm, NewsletterForm
# ======================================================================================================================
# نمایش و پردازش فرم تماس با ما
class ContactView(FormView):
    # قالب صفحه تماس
    template_name = 'contacts/contacts.html'

    # فرم استفاده‌شده در این ویو
    form_class = ContactForm

    # مسیر بعد از ارسال موفق فرم
    success_url = reverse_lazy('contact:contact-us')

    # ذخیره اطلاعات فرم و نمایش پیام موفقیت
    def form_valid(self, form):
        form.save()
        messages.success(
            self.request,
            'پیام شما با موفقیت ارسال شد.'
        )
        return super().form_valid(form)
# ======================================================================================================================
# عضویت در خبرنامه
class NewsletterSubscribeView(View):

    # پردازش درخواست POST برای عضویت
    def post(self, request, *args, **kwargs):
        form = NewsletterForm(request.POST)

        # اگر فرم معتبر باشد ذخیره کن
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "عضویت شما در خبرنامه انجام شد."
            )
        else:
            messages.error(
                request,
                "ایمیل معتبر وارد کنید یا قبلاً عضو شده‌اید."
            )

        # برگشت به صفحه قبلی
        return redirect(request.META.get("HTTP_REFERER", "/"))
# ======================================================================================================================