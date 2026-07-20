from django import forms
from .models import ProductReviewModels
# ======================================================================================================================
# فرم ثبت نظر برای محصول
class ProductReviewForm(forms.ModelForm):

    class Meta:
        model = ProductReviewModels
        fields = ["full_name", "email", "rating", "comment"]
        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "نام شما",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "ایمیل شما",
            }),
            "rating": forms.HiddenInput(),
            "comment": forms.Textarea(attrs={
                "class": "form-control address",
                "placeholder": "نظر دهید",
                "rows": 5,
            }),
        }
# ======================================================================================================================