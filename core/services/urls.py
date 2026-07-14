from django.urls import path
from .views import (
    ServiceListView,
    ServiceDetailView,
)
# ======================================================================================================================
# نام فضای آدرس‌دهی اپلیکیشن خدمات
app_name = "services"

# مسیرهای مربوط به خدمات
urlpatterns = [

    # صفحه لیست خدمات
    path(
        "services-list/",
        ServiceListView.as_view(),
        name="service-list",
    ),

    # صفحه جزئیات خدمت
    path(
        "services/<slug:slug>/",
        ServiceDetailView.as_view(),
        name="service-detail",
    ),
]

# ======================================================================================================================
