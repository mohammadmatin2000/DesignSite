from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from accounts.models import Profile
# ======================================================================================================================
# فرم ویرایش پروفایل مشتری
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "phone_number", "image"]
# ======================================================================================================================
# فرم تغییر رمز عبور (بر پایه فرم استاندارد جنگو، سازگار با مدل کاربری سفارشی)
class CustomerPasswordChangeForm(PasswordChangeForm):
    pass
# ======================================================================================================================