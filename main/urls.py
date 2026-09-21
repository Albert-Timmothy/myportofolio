from django.urls import path

from main.views import (
    create_project,
    create_skill,
    delete_project,
    delete_skill,
    get_awards_json,
    get_experiences_json,
    get_projects_json,
    get_skills_json,
    show_award,
    show_experience,
    show_main,
    show_projects,
    show_skills,
    update_project,
    update_skill,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("awards/", show_award, name="show_award"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/", show_projects, name="show_projects"),
    path("projects/<uuid:project_id>/edit/", update_project, name="update_project"),
    path("projects/<uuid:project_id>/delete/", delete_project, name="delete_project"),
    path("skills/", show_skills, name="show_skills"),
    path("skills/add/", create_skill, name="create_skill"),
    path("skills/<uuid:skill_id>/edit/", update_skill, name="update_skill"),
    path("skills/<uuid:skill_id>/delete/", delete_skill, name="delete_skill"),
    path("api/awards/", get_awards_json, name="get_awards_json"),
    path("api/experiences/", get_experiences_json, name="get_experiences_json"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("api/skills/", get_skills_json, name="get_skills_json"),
]