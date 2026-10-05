from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

import datetime

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from main.forms import ProjectForm, SkillForm
from main.models import Award, Experience, Project, Skill

OWNER_NAME = "Albert Timmothy Ariajaya"


def _json_response(queryset, fields=None):
    """Serialisasi queryset model ke JSON lalu bungkus sebagai HttpResponse."""
    return HttpResponse(
        serializers.serialize("json", queryset, fields=fields),
        content_type="application/json",
    )


def show_main(request):
    last_login = request.COOKIES.get(
        "last_login", "Belum ada sesi login / Cookie tidak ditemukan."
    )
    context = {
        "name": OWNER_NAME,
        "npm": "2506656381",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Information Systems undergraduate student..."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)
    
def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": OWNER_NAME,
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie(
            "last_login", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        return response

    context = {
        "name": OWNER_NAME,
        "form": form,
    }
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie("last_login")
    return response

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

@login_required(login_url="/login/")
def create_project(request):
    if not request.user.has_perm("main.add_project"):
        raise PermissionDenied

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


@require_POST
def create_project_ajax(request):
    # Tidak memakai @login_required agar pengunjung yang belum login
    # mendapat JSON 403 (bukan redirect ke halaman login yang bisa dibaca fetch sebagai 200).
    if not request.user.has_perm("main.add_project"):
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)

    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@login_required(login_url="/login/")
def update_project(request, project_id):
    if not request.user.has_perm("main.change_project"):
        raise PermissionDenied

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


@login_required(login_url="/login/")
def delete_project(request, project_id):
    if not request.user.has_perm("main.delete_project"):
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")

def show_projects(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": OWNER_NAME,
        "title_query": title_query,
        "form": ProjectForm(),
    }
    return render(request, "project.html", context)


def get_projects_json(request):
    """Data proyek dalam format JSON, mendukung filter ?title=."""
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related("starred_by").all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = (
            request.user in starred_users if request.user.is_authenticated else False
        )

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "tech_stack": project.tech_stack,
                "project_url": project.project_url,
                "project_image_url": project.project_image_url,
                "star_count": len(starred_users),
                "is_starred": is_starred,
            },
        })

    return JsonResponse(data, safe=False)


@login_required(login_url="/login/")
@require_POST
def toggle_star(request, project_id):
    """Beri atau batalkan star dari user yang sedang login (maks. satu per user)."""
    project = get_object_or_404(Project, pk=project_id)

    if project.starred_by.filter(pk=request.user.pk).exists():
        project.starred_by.remove(request.user)
    else:
        project.starred_by.add(request.user)

    return redirect("main:show_projects")


# ---------- Skills & Tools ----------

def _filtered_skills(request):
    """Query bersama untuk halaman Skills dan endpoint AJAX."""
    name_query = request.GET.get("name", "").strip()
    category = request.GET.get("category", "").strip()
    skills = Skill.objects.prefetch_related("starred_by").all()

    if name_query:
        skills = skills.filter(name__icontains=name_query)
    if category in dict(Skill.CATEGORY_CHOICES):
        skills = skills.filter(category=category)

    return skills


def get_skills_json(request):
    """Data publik dan status star tanpa mengekspos identitas pemberi star."""
    data = []
    for skill in _filtered_skills(request):
        starred_users = list(skill.starred_by.all())
        data.append({
            "pk": str(skill.pk),
            "fields": {
                "name": skill.name,
                "category": skill.category,
                "category_display": skill.get_category_display(),
                "proficiency": skill.proficiency,
                "proficiency_display": skill.get_proficiency_display(),
                "description": skill.description,
                "icon_url": skill.icon_url,
                "is_featured": skill.is_featured,
                "created_at": skill.created_at,
                "updated_at": skill.updated_at,
                "star_count": len(starred_users),
                "is_starred": request.user.is_authenticated and any(
                    user.pk == request.user.pk for user in starred_users
                ),
            },
        })
    return JsonResponse(data, safe=False)


def show_skills(request):
    context = {
        "name": OWNER_NAME,
        "form": SkillForm(),
        "name_query": request.GET.get("name", "").strip(),
        "selected_category": request.GET.get("category", "").strip(),
        "category_choices": Skill.CATEGORY_CHOICES,
    }
    return render(request, "skills.html", context)


@require_POST
def create_skill_ajax(request):
    # JSON 403, bukan redirect login yang akan diikuti oleh fetch().
    if not request.user.has_perm("main.add_skill"):
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan skill."},
            status=403,
        )

    form = SkillForm(request.POST)
    if form.is_valid():
        skill = form.save()
        return JsonResponse(
            {"message": "Skill berhasil ditambahkan.", "pk": str(skill.pk)},
            status=201,
        )
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)


@login_required(login_url="/login/")
def create_skill(request):
    if not request.user.has_perm("main.add_skill"):
        raise PermissionDenied

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


@login_required(login_url="/login/")
def update_skill(request, skill_id):
    if not request.user.has_perm("main.change_skill"):
        raise PermissionDenied

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


@login_required(login_url="/login/")
@require_POST
def delete_skill(request, skill_id):
    if not request.user.has_perm("main.delete_skill"):
        raise PermissionDenied

    skill = get_object_or_404(Skill, pk=skill_id)
    skill.delete()
    messages.success(request, "Skill berhasil dihapus!")
    return redirect("main:show_skills")


@login_required(login_url="/login/")
@require_POST
def toggle_skill_star(request, skill_id):
    """Beri atau batalkan star skill dari user yang login (maks. satu per user)."""
    skill = get_object_or_404(Skill, pk=skill_id)

    if skill.starred_by.filter(pk=request.user.pk).exists():
        skill.starred_by.remove(request.user)
    else:
        skill.starred_by.add(request.user)

    return redirect("main:show_skills")