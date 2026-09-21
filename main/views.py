from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from main.forms import ProjectForm, SkillForm
from main.models import Award, Experience, Project, Skill

OWNER_NAME = "Albert Timmothy Ariajaya"


def _json_response(queryset):
    """Serialisasi queryset model ke JSON lalu bungkus sebagai HttpResponse."""
    return HttpResponse(
        serializers.serialize("json", queryset),
        content_type="application/json",
    )


def show_main(request):
    context = {
        "name": OWNER_NAME,
        "npm": "2506656381",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Information Systems undergraduate student of Universitas Indonesia with strong leadership, communication, dynamic and problem-solving skills. Quick learner with a collaborative mindset, analytical thinking and curious on new innovation. Adapting to new challenges while continuously expanding knowledge and expertise."
        ),
    }
    return render(request, "index.html", context)


def show_award(request):
    context = {
        "name": OWNER_NAME,
        "award_list": Award.objects.all(),
    }
    return render(request, "award.html", context)


def get_awards_json(request):
    return _json_response(Award.objects.all())


def show_experience(request):
    context = {
        "name": OWNER_NAME,
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def get_experiences_json(request):
    return _json_response(Experience.objects.all())


# ---------- Projects ----------

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": OWNER_NAME,
        "form": form,
        "form_title": "Tambah Proyek",
        "submit_label": "Tambah Project",
    }
    return render(request, "projects_form.html", context)


def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None, instance=project)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek berhasil diperbarui!")
        return redirect("main:show_projects")

    context = {
        "name": OWNER_NAME,
        "form": form,
        "form_title": "Edit Proyek",
        "submit_label": "Simpan Perubahan",
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
        "name": OWNER_NAME,
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "project.html", context)


def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    return _json_response(projects)


def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")


# ---------- Skills & Tools ----------

def get_skills_json(request):
    """Data skill dalam format JSON. Mendukung filter ?name= dan ?category=."""
    name_query = request.GET.get("name", "").strip()
    category = request.GET.get("category", "").strip()
    skills = Skill.objects.all()

    if name_query:
        skills = skills.filter(name__icontains=name_query)
    if category in dict(Skill.CATEGORY_CHOICES):
        skills = skills.filter(category=category)

    return _json_response(skills)


def show_skills(request):
    # Ambil data lewat JSON, lalu deserialisasi kembali menjadi objek Skill.
    json_response = get_skills_json(request)
    deserialized = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    skills = [item.object for item in deserialized]

    context = {
        "name": OWNER_NAME,
        "skill_list": skills,
        "name_query": request.GET.get("name", "").strip(),
        "selected_category": request.GET.get("category", "").strip(),
        "category_choices": Skill.CATEGORY_CHOICES,
    }
    return render(request, "skills.html", context)


def create_skill(request):
    form = SkillForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skill baru berhasil ditambahkan!")
        return redirect("main:show_skills")

    context = {
        "name": OWNER_NAME,
        "form": form,
        "form_title": "Tambah Skill & Tool",
        "submit_label": "Tambah Skill",
    }
    return render(request, "skill_form.html", context)


def update_skill(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)
    form = SkillForm(request.POST or None, instance=skill)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skill berhasil diperbarui!")
        return redirect("main:show_skills")

    context = {
        "name": OWNER_NAME,
        "form": form,
        "form_title": "Edit Skill & Tool",
        "submit_label": "Simpan Perubahan",
    }
    return render(request, "skill_form.html", context)


@require_POST
def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)
    skill.delete()
    messages.success(request, "Skill berhasil dihapus!")
    return redirect("main:show_skills")