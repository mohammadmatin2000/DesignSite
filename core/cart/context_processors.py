from .models import CartModel
# ======================================================================================================================
def cart_context(request):
    if request.user.is_authenticated:
        cart = CartModel.objects.filter(user=request.user).first()
        if cart:
            return {
                "cart_items": cart.items.select_related("product"),
                "cart_items_count": cart.total_quantity,
                "cart_total": cart.total_price,
            }

    return {
        "cart_items": None,
        "cart_items_count": 0,
        "cart_total": 0,
    }
# ======================================================================================================================