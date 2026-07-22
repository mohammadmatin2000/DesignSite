from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from accounts.models import UserType
# ======================================================================================================================
class DashboardHomeView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):

        print("User type:", request.user.type)

        if request.user.type == UserType.customer:
            return redirect("dashboard:customer:home")

        elif request.user.type in (UserType.admin, UserType.superuser):
            return redirect("dashboard:admin:home")

        print("Redirecting to login because of unknown user type.")
        return redirect("accounts:login")
# ======================================================================================================================