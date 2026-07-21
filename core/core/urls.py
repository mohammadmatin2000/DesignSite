from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings



# ======================================================================================================================
urlpatterns = [
    path("", include("index.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("contacts/", include("contacts.urls")),
    path("projects/", include("projects.urls")),
    path("services/", include("services.urls")),
    path("blog/", include("blog.urls")),
    path("team/", include("team.urls")),
    path("shop/", include("shop.urls")),
    path("cart/", include("cart.urls")),
    path('captcha/', include('captcha.urls')),
]
# ======================================================================================================================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# ======================================================================================================================