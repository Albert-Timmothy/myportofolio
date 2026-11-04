from django.urls import path

from main.api_views import project_detail, project_list, project_star

app_name = "api"

urlpatterns = [
    path("projects/", project_list, name="project-list"),
    path("projects/<uuid:project_id>/", project_detail, name="project-detail"),
    path("projects/<uuid:project_id>/star/", project_star, name="project-star"),
]
