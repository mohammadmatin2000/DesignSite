from .models import CommentModel
from django import forms
from captcha.fields import CaptchaField
# ======================================================================================================================
# فرم ثبت نظر روی مقالات وبلاگ
class CommentForm(forms.ModelForm):
    # فیلد کد امنیتی برای جلوگیری از ارسال اسپم
    captcha = CaptchaField()
    class Meta:
        model = CommentModel
        fields = ["fullname", "email", "website", "message","captcha"]
        widgets = {
            "fullname": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "نام*",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "ایمیل*",
            }),
            "website": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "وب سایت",
            }),
            "message": forms.Textarea(attrs={
                "class": "form-control address",
                "placeholder": "نظر*",
                "rows": 8,
                "cols": 30,
            }),
        }
# ======================================================================================================================