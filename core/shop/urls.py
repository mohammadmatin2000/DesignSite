from django.urls import path
from .views import ProductListView, ProductDetailView
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
        "products-detail/<slug:slug>/",
        ProductDetailView.as_view(),
        name="shop-detail"
    ),

]
# ======================================================================================================================