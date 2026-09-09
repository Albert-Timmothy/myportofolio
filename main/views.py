from django.shortcuts import render

from main.models import Experience


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


def show_experience(request):
    context = {
        "name": "Albert Timmmothy Ariajaya",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

