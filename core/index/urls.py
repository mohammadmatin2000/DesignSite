from .views import IndexView,SearchView
from django.urls import path
# ======================================================================================================================

# مسیرهای مربوط به صفحه اصلی سایت
app_name = "index"

urlpatterns = [
    # نمایش صفحه اصلی
    path("", IndexView.as_view(), name="index"),
    path("search/", SearchView.as_view(), name="search"),
]

# ======================================================================================================================