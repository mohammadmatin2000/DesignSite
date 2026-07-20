from django.urls import path,reverse_lazy
from django.contrib.auth import views as auth_views
from .views import LoginView, LogoutView, SignupView
from .forms import SetPasswordForm
# ======================================================================================================================
app_name = 'accounts'
# ======================================================================================================================
# تعریف مسیرهای مربوط به احراز هویت و مدیریت حساب کاربری
urlpatterns = [

    # مسیر ثبت‌نام کاربران
    path("signup/", SignupView.as_view(), name="signup"),

    # مسیر ورود کاربران
    path("login/", LoginView.as_view(), name="login"),

    # مسیر خروج کاربران
    path("logout/", LogoutView.as_view(), name="logout"),

    # درخواست بازیابی رمز عبور از طریق ایمیل
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/reset-password/reset_password.html",
            email_template_name="accounts/reset-password/password_reset_email.html",
            subject_template_name="accounts/reset-password/password_reset_subject.txt",
            success_url= reverse_lazy("accounts:password_reset_done"),
        ),
        name="password_reset",
    ),

    # نمایش پیام ارسال لینک بازیابی رمز عبور
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/reset-password/reset_password_done.html"
        ),
        name="password_reset_done",
    ),

    # تأیید لینک بازیابی و تعیین رمز عبور جدید
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/reset-password/reset_password_form.html",
            form_class=SetPasswordForm,
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),

    # نمایش پیام موفقیت‌آمیز بودن تغییر رمز عبور
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/reset-password/reset_password_complete.html"
        ),
        name="password_reset_complete",
    ),
]
# ======================================================================================================================