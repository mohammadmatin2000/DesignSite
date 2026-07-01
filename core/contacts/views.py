from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import ContactForm
# ======================================================================================================================
# مدیریت نمایش و پردازش فرم تماس با ما
class ContactView(FormView):

    # قالب مورد استفاده برای نمایش فرم
    template_name = 'contacts/contacts.html'

    # فرم مرتبط با صفحه تماس
    form_class = ContactForm

    # آدرس هدایت پس از ارسال موفق فرم
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