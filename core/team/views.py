from django.views.generic import ListView, DetailView
from .models import TeamModels
# ======================================================================================================================
# نمایش اعضای تیم
class TeamListView(ListView):

    model = TeamModels

    template_name = "team/team.html"

    context_object_name = "teams"

    def get_queryset(self):
        return TeamModels.objects.filter(is_active=True)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # اعضایی که is_manager روشونه، برای نمایش در بخش نظرات
        context["managers"] = TeamModels.objects.filter(
            is_active=True,
            is_manager=True
        )

        return context
# ======================================================================================================================
# نمایش جزئیات عضو تیم
class TeamDetailView(DetailView):

    model = TeamModels

    template_name = "team/team-detail.html"

    context_object_name = "team"
# ======================================================================================================================