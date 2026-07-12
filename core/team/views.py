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
# ======================================================================================================================
# نمایش جزئیات عضو تیم
class TeamDetailView(DetailView):

    model = TeamModels

    template_name = "team/team_detail.html"

    context_object_name = "team"
# ======================================================================================================================