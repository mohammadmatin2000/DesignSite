from django.urls import path
from .views import TeamListView, TeamDetailView
# ======================================================================================================================
app_name = "team"

urlpatterns = [

    path(
        "team/",
        TeamListView.as_view(),
        name="team"
    ),

    path(
        "team/<int:pk>/",
        TeamDetailView.as_view(),
        name="team_detail"
    ),

]
# ======================================================================================================================