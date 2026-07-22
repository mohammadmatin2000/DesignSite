from django.urls import path
from . import views
# ======================================================================================================================
app_name = "customer"
# ======================================================================================================================
urlpatterns = [
    path("home/", views.CustomerHomeView.as_view(), name="home"),

    path("profile/", views.CustomerProfileView.as_view(), name="profile"),
    path("security/", views.CustomerSecurityView.as_view(), name="security"),

    path("order/", views.CustomerOrderListView.as_view(), name="order-list"),
    path("order/<int:pk>/", views.CustomerOrderDetailView.as_view(), name="order-detail"),

    path("messages/", views.CustomerMessageListView.as_view(), name="message-list"),
    path("messages/<int:pk>/", views.CustomerMessageDetailView.as_view(), name="message-detail"),

    path("wishlist/", views.CustomerWishlistView.as_view(), name="wishlist"),
    path("wishlist/<int:pk>/delete/", views.CustomerWishlistDeleteView.as_view(), name="wishlist-delete"),
]
# ======================================================================================================================