from django import forms
from captcha.fields import CaptchaField
from .models import ContactMessageModel
# ======================================================================================================================
# فرم ثبت و ارسال پیام کاربران همراه با کد امنیتی
class ContactForm(forms.ModelForm):

    # فیلد کد امنیتی برای جلوگیری از ارسال اسپم
    captcha = CaptchaField()

    class Meta:
        # مدل مرتبط با فرم
        model = ContactMessageModel

        # فیلدهای قابل نمایش در فرم
        fields = (
            'name',
            'email',
            'message',
            'phone_number',
            'service'
        )
        # سفارشی‌سازی ظاهر فیلدها
        widgets = {
            # تنظیم تعداد سطرهای فیلد پیام
            "message": forms.Textarea(attrs={'rows': 5}),
        }
# ======================================================================================================================