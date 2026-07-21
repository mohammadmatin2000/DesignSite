from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from order.models import OrderModel
from .models import PaymentModel
from .services import zarinpal_request_payment, zarinpal_verify_payment
# ======================================================================================================================
# شروع فرآیند پرداخت و ریدایرکت به درگاه زرین‌پال
class PaymentRequestView(LoginRequiredMixin, View):

    def post(self, request, order_id):
        order = get_object_or_404(OrderModel, id=order_id, user=request.user)

        if order.status != "pending":
            messages.info(request, "این سفارش قبلاً پرداخت شده یا قابل پرداخت نیست.")
            return redirect("order:order-detail", pk=order.id)

        amount = order.total_price
        description = f"پرداخت سفارش شماره {order.id}"

        authority, payment_url = zarinpal_request_payment(
            request=request,
            amount=amount,
            description=description,
            mobile=order.phone,
        )

        if not authority:
            messages.error(request, "خطا در اتصال به درگاه پرداخت. لطفاً دوباره تلاش کنید.")
            return redirect("order:order-detail", pk=order.id)

        PaymentModel.objects.create(
            order=order,
            amount=amount,
            authority=authority,
            status="pending",
        )

        return redirect(payment_url)
# ======================================================================================================================
# دریافت بازگشت از درگاه و تایید نهایی تراکنش
class PaymentVerifyView(LoginRequiredMixin, View):

    def get(self, request):
        authority = request.GET.get("Authority")
        zarinpal_status = request.GET.get("Status")

        payment = PaymentModel.objects.filter(authority=authority, order__user=request.user).first()

        if not payment:
            messages.error(request, "تراکنش یافت نشد.")
            return redirect("order:order-list")

        if zarinpal_status != "OK":
            payment.status = "failed"
            payment.save()
            messages.error(request, "پرداخت توسط شما لغو شد.")
            return redirect("order:order-detail", pk=payment.order.id)

        is_verified, ref_id = zarinpal_verify_payment(amount=payment.amount, authority=authority)

        if is_verified:
            payment.status = "success"
            payment.ref_id = ref_id
            payment.save()

            payment.order.status = "paid"
            payment.order.save()

            messages.success(request, f"پرداخت با موفقیت انجام شد. کد پیگیری: {ref_id}")
        else:
            payment.status = "failed"
            payment.save()
            messages.error(request, "تایید پرداخت ناموفق بود.")

        return redirect("order:order-detail", pk=payment.order.id)
# ======================================================================================================================