from django.views.generic import ListView, DetailView
from .models import ProjectModel, ProjectDetailModels
# ======================================================================================================================
# نمایش لیست پروژه‌ها
class ProjectListView(ListView):
    model = ProjectModel
    template_name = "projects/projects.html"
    context_object_name = "projects"
    ordering = ["-created_date"]
# ======================================================================================================================
# نمایش جزئیات هر پروژه
class ProjectDetailView(DetailView):
    model = ProjectDetailModels
    template_name = "projects/project-detail.html"
    context_object_name = "project"
    slug_field = "slug"
    slug_url_kwarg = "slug"
# ======================================================================================================================