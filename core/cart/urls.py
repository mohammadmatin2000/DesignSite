from django.urls import path
from . import views
# ======================================================================================================================
app_name = "cart"
# ======================================================================================================================
urlpatterns = [
    path("cart/", views.CartView.as_view(), name="cart-detail"),
    path("add/<str:slug>/", views.CartAddView.as_view(), name="cart-add"),
    path("remove/<int:item_id>/", views.CartRemoveView.as_view(), name="cart-remove"),
    path("update/<int:item_id>/", views.CartUpdateView.as_view(), name="cart-update"),
]
# ======================================================================================================================