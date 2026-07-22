from django.views.generic import TemplateView, UpdateView, ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from dashboard.permission import HasCustomerPermission
from order.models import OrderModel
from contacts.models import ContactMessageModel
from shop.models import WishlistModel
from .forms import CustomerProfileForm, CustomerPasswordChangeForm
# ======================================================================================================================
# میکسین مشترک برای همه‌ی ویوهای مشتری
class CustomerRequiredMixin(LoginRequiredMixin, HasCustomerPermission):
    pass
# ======================================================================================================================
# صفحه اصلی داشبورد مشتری
class CustomerHomeView(CustomerRequiredMixin, TemplateView):
    template_name = "dashboard/customer/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_orders"] = OrderModel.objects.filter(user=self.request.user)[:5]
        context["total_orders"] = OrderModel.objects.filter(user=self.request.user).count()
        context["total_wishlist"] = WishlistModel.objects.filter(user=self.request.user).count()
        return context
# ======================================================================================================================
# ---------------------------- پروفایل ----------------------------
class CustomerProfileView(CustomerRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = CustomerProfileForm
    template_name = "dashboard/customer/profile/profile.html"
    success_url = reverse_lazy("dashboard:customer:profile")
    success_message = "اطلاعات پروفایل با موفقیت بروزرسانی شد."

    def get_object(self, queryset=None):
        return self.request.user.user_profile
# ======================================================================================================================
class CustomerSecurityView(CustomerRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    form_class = CustomerPasswordChangeForm
    template_name = "dashboard/customer/profile/security.html"
    success_url = reverse_lazy("dashboard:customer:security")
    success_message = "رمز عبور با موفقیت تغییر کرد."
# ======================================================================================================================
# ---------------------------- سفارش‌ها ----------------------------
class CustomerOrderListView(CustomerRequiredMixin, ListView):
    model = OrderModel
    template_name = "dashboard/customer/order/order-list.html"
    context_object_name = "order"
    paginate_by = 10

    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user)
# ======================================================================================================================
class CustomerOrderDetailView(CustomerRequiredMixin, DetailView):
    model = OrderModel
    template_name = "dashboard/customer/order/order-detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user)
# ======================================================================================================================
# ---------------------------- پیام‌ها ----------------------------
class CustomerMessageListView(CustomerRequiredMixin, ListView):
    model = ContactMessageModel
    template_name = "dashboard/customer/messages/message-list.html"
    context_object_name = "contact_messages"
    paginate_by = 10

    def get_queryset(self):
        return ContactMessageModel.objects.filter(user=self.request.user)
# ======================================================================================================================
class CustomerMessageDetailView(CustomerRequiredMixin, DetailView):
    model = ContactMessageModel
    template_name = "dashboard/customer/messages/message-detail.html"
    context_object_name = "contact_message"

    def get_queryset(self):
        return ContactMessageModel.objects.filter(user=self.request.user)
# ======================================================================================================================
# ---------------------------- علاقه‌مندی‌ها ----------------------------
class CustomerWishlistView(CustomerRequiredMixin, ListView):
    model = WishlistModel
    template_name = "dashboard/customer/wishlist/wishlist.html"
    context_object_name = "wishlist_items"
    paginate_by = 12

    def get_queryset(self):
        return WishlistModel.objects.filter(user=self.request.user).select_related("product")
# ======================================================================================================================
class CustomerWishlistDeleteView(CustomerRequiredMixin, View):

    def post(self, request, pk):
        item = get_object_or_404(WishlistModel, pk=pk, user=request.user)
        item.delete()
        messages.success(request, "محصول از لیست علاقه‌مندی‌ها حذف شد.")
        return redirect("dashboard:customer:wishlist")
# ======================================================================================================================