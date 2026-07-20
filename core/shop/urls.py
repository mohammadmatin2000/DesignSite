from django.urls import path
from .views import ProductListView, ProductDetailView, WishlistToggleView
# ======================================================================================================================
app_name = "shop"
# ======================================================================================================================
urlpatterns = [

    # صفحه محصولات
    path(
        "products/",
        ProductListView.as_view(),
        name="shop-list"
    ),

    # جزئیات محصول
    path(
        "products-detail/<str:slug>/",
        ProductDetailView.as_view(),
        name="shop-detail"
    ),
    path("<str:slug>/wishlist-toggle/", WishlistToggleView.as_view(), name="wishlist-toggle"),


]
# ======================================================================================================================