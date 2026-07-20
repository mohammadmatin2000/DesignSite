from django.contrib.auth import views as auth_views
from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomAuthenticationForm, CustomSignupForm
# ======================================================================================================================
# مدیریت فرآیند ثبت‌نام کاربران
class SignupView(View):

    # نمایش فرم ثبت‌نام
    def get(self, request):
        form = CustomSignupForm()
        return render(request, "accounts/signup.html", {"form": form})

    # پردازش اطلاعات فرم و ایجاد کاربر جدید
    def post(self, request):
        form = CustomSignupForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "ثبت‌نام با موفقیت انجام شد! اکنون وارد شوید."
            )
            return redirect("accounts:login")

        return render(request, "accounts/signup.html", {"form": form})
# ======================================================================================================================
# مدیریت ورود کاربران به سیستم
class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True
    form_class = CustomAuthenticationForm
# ======================================================================================================================
# مدیریت خروج کاربران از سیستم
class LogoutView(auth_views.LogoutView):
    next_page = "accounts:login"
# ======================================================================================================================
