from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from main.api_views import api_logout

from main.api_views import project_detail, project_list, project_star, skill_detail, skill_list, skill_star

app_name = "api"

urlpatterns = [
    path("auth/token/", obtain_auth_token, name="token"),
    path("auth/logout/", api_logout, name="logout"),
    path("skills/", skill_list, name="skill-list"),
    path("skills/<uuid:skill_id>/", skill_detail, name="skill-detail"),
    path("skills/<uuid:skill_id>/star/", skill_star, name="skill-star"),
    path("projects/", project_list, name="project-list"),
    path("projects/<uuid:project_id>/", project_detail, name="project-detail"),
    path("projects/<uuid:project_id>/star/", project_star, name="project-star"),
]
