from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import DetailView
from shop.models import ProductModels,WishlistModel
from .models import CartModel, CartItemModel
# ======================================================================================================================
# نمایش صفحه سبد خرید
class CartView(LoginRequiredMixin, DetailView):
    model = CartModel
    template_name = "cart/cart.html"
    context_object_name = "cart"

    def get_object(self, queryset=None):
        cart, created = CartModel.objects.get_or_create(user=self.request.user)
        return cart

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart_items"] = self.object.items.select_related("product")
        context["wishlist_ids"] = set(WishlistModel.objects.filter(user=self.request.user).values_list("product_id", flat=True))
        return context
# ======================================================================================================================
# افزودن محصول به سبد خرید
class CartAddView(LoginRequiredMixin, View):

    def get(self, request, slug):
        product = get_object_or_404(ProductModels, slug=slug)
        cart, created = CartModel.objects.get_or_create(user=request.user)

        item, item_created = CartItemModel.objects.get_or_create(
            cart=cart,
            product=product,
        )
        if not item_created:
            item.quantity += 1
            item.save()

        return redirect("cart:cart-detail")
# ======================================================================================================================
# افزایش / کاهش تعداد آیتم سبد خرید
@method_decorator(require_POST, name="dispatch")
class CartUpdateView(LoginRequiredMixin, View):

    def post(self, request, item_id):
        item = get_object_or_404(CartItemModel, id=item_id, cart__user=request.user)
        action = request.POST.get("action")

        if action == "increase":
            item.quantity += 1
            item.save()

        elif action == "decrease":
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()

        return redirect("cart:cart-detail")
# ======================================================================================================================
# حذف آیتم از سبد خرید
@method_decorator(require_POST, name="dispatch")
class CartRemoveView(LoginRequiredMixin, View):

    def post(self, request, item_id):
        item = get_object_or_404(CartItemModel, id=item_id, cart__user=request.user)
        item.delete()
        return redirect("cart:cart-detail")
# ======================================================================================================================