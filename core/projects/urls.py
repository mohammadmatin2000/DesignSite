from django.urls import path
from .views import (
    ProjectListView,
    ProjectDetailView,
)
# ======================================================================================================================
# نام فضای آدرس‌دهی اپلیکیشن پروژه‌ها
app_name = "projects"

# تعریف مسیرهای مربوط به پروژه‌ها
urlpatterns = [

    # نمایش لیست پروژه‌ها
    path(
        "projects-list/",
        ProjectListView.as_view(),
        name="project-list"
    ),

    # نمایش جزئیات پروژه
    path(
        "projects/<slug:slug>/",
        ProjectDetailView.as_view(),
        name="project-detail"
    ),
]
# ======================================================================================================================