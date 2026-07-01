from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
User = get_user_model()
# ======================================================================================================================
# فرم ثبت‌نام کاربران همراه با اعتبارسنجی ایمیل، رمز عبور و کپچا
class CustomSignupForm(forms.ModelForm):
    password1 = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="تأیید رمز عبور",
        widget=forms.PasswordInput
    )
    captcha = CaptchaField(label="کد امنیتی")

    class Meta:
        model = User
        fields = ["email"]

    # بررسی تکراری نبودن ایمیل
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("این ایمیل قبلاً ثبت شده است.")
        return email

    # بررسی یکسان بودن رمز عبور و تکرار آن
    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:
            raise ValidationError("رمز عبور و تکرار آن یکسان نیستند.")

        return cleaned_data

    # ایجاد و ذخیره کاربر جدید با رمز عبور هش شده
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
# ======================================================================================================================
# فرم ورود کاربران همراه با کپچا و بررسی وضعیت فعال بودن حساب
class CustomAuthenticationForm(AuthenticationForm):
    captcha = CaptchaField(label="کد امنیتی")

    # جلوگیری از ورود کاربران غیرفعال
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                "حساب کاربری شما غیرفعال است.",
                code="inactive"
            )
# ======================================================================================================================
# فرم تعیین یا تغییر رمز عبور بدون نیاز به وارد کردن رمز قبلی
class SetPasswordForm(forms.Form):

    # پیام‌های خطای سفارشی فرم
    error_messages = {
        "password_mismatch": _("رمز عبور و تکرار آن با یکدیگر مطابقت ندارند."),
    }

    # فیلد دریافت رمز عبور جدید
    new_password1 = forms.CharField(
        label="رمز عبور جدید",
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}
        ),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    # فیلد دریافت تکرار رمز عبور جدید
    new_password2 = forms.CharField(
        label="تکرار رمز عبور جدید",
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "new-password", "class": "form-control"}
        ),
    )

    # مقداردهی اولیه و دریافت کاربر
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    # بررسی تطابق و اعتبارسنجی رمز عبور جدید
    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )

        password_validation.validate_password(password2, self.user)
        return password2

    # ذخیره رمز عبور جدید به صورت رمزنگاری شده
    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)

        if commit:
            self.user.save()

        return self.user
# ======================================================================================================================