from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, View
from cart.models import CartModel
from .models import OrderModel, OrderItemModel
# ======================================================================================================================
# صفحه چک‌اوت (نمایش فرم + ثبت سفارش)
class CheckoutView(LoginRequiredMixin, View):
    template_name = "order/checkout.html"

    def get(self, request):
        from django.shortcuts import render
        cart = CartModel.objects.filter(user=request.user).first()

        if not cart or not cart.items.exists():
            messages.warning(request, "سبد خرید شما خالی است.")
            return redirect("shop:shop-list")

        context = {
            "cart": cart,
            "cart_items": cart.items.select_related("product"),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        cart = CartModel.objects.filter(user=request.user).first()

        if not cart or not cart.items.exists():
            messages.warning(request, "سبد خرید شما خالی است.")
            return redirect("shop:shop-list")

        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        postal_code = request.POST.get("postal_code")
        note = request.POST.get("note")

        order = OrderModel.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            address=address,
            postal_code=postal_code,
            note=note,
        )

        for cart_item in cart.items.select_related("product"):
            OrderItemModel.objects.create(
                order=order,
                product=cart_item.product,
                product_title=cart_item.product.title,
                price=cart_item.product.price,
                quantity=cart_item.quantity,
            )

        # خالی کردن سبد خرید پس از ثبت سفارش
        cart.items.all().delete()

        messages.success(request, "سفارش شما با موفقیت ثبت شد.")
        return redirect("order:order-detail", pk=order.id)
# ======================================================================================================================
# لیست سفارش‌های کاربر
class OrderListView(LoginRequiredMixin, ListView):
    model = OrderModel
    template_name = "order/order-list.html"
    context_object_name = "order"
    paginate_by = 10

    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user)
# ======================================================================================================================
# جزئیات یک سفارش
class OrderDetailView(LoginRequiredMixin, DetailView):
    model = OrderModel
    template_name = "order/order-detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return OrderModel.objects.filter(user=self.request.user)
# ======================================================================================================================