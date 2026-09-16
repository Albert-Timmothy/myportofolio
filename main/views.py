from django.shortcuts import render
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from main.models import Experience, Award, Project
from main.forms import ProjectForm

def show_main(request):
    context = {
        "name": "Albert Timmmothy Ariajaya",
        "npm": "2506656381",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Information Systems undergraduate student of Universitas Indonesia with strong leadership, communication, dynamic and problem-solving skills. Quick learner with a collaborative mindset, analytical thinking and curious on new innovation. Adapting to new challenges while continuously expanding knowledge and expertise."
        ),
    }
    return render(request, "index.html", context)

def show_award(request):
    context = {
        "name": "Albert Timmmothy Ariajaya",
        "award_list": Award.objects.all(),
    }
    return render(request, "award.html", context)

def show_experience(request):
    context = {
        "name": "Albert Timmmothy Ariajaya",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Albert Timmmothy Ariajaya",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Albert Timmmothy Ariajaya",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "project.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")