from django.db import migrations


def create_initial_portfolio_data(apps, schema_editor):
    Award = apps.get_model("main", "Award")
    Experience = apps.get_model("main", "Experience")

    awards = [
        {
            "title": "Winner, RISTEK Hackathon 2026",
            "organizer": "RISTEK Fasilkom UI & RISNOVMAS",
            "date": "Aug 2026",
            "description": (
                "Won first place in a hackathon focused on innovation, product "
                "thinking, and digital solution development."
            ),
        },
        {
            "title": "Best Exhibition Awardee, RISTEK Hackathon 2026",
            "organizer": "RISTEK Fasilkom UI & RISNOVMAS",
            "date": "Aug 2026",
            "description": (
                "Recognized for presenting a strong project showcase and "
                "communicating the solution clearly during the exhibition."
            ),
        },
        {
            "title": "Top National Finalist, Hackathon Digital Cooperatives Expo 2026",
            "organizer": "Kementerian Koperasi Republik Indonesia & PEBS FEB UI",
            "date": "Jul 2026",
            "description": (
                "Selected as a national finalist for developing a digital cooperative "
                "solution with practical business and technology impact."
            ),
        },
        {
            "title": "Best 1st Graduation Student 2026",
            "organizer": "SMA Negeri 66 Jakarta",
            "date": "May 2026",
            "description": (
                "Graduated with the highest graduation score, achieving 91.47 out "
                "of 100."
            ),
        },
    ]

    experiences = [
        {
            "title": "Lecturer Assistant, Business Management",
            "description": (
                "Assisted in delivering course material and supporting student "
                "learning; coordinated grading and communication between faculty "
                "and students."
            ),
            "category": "part-time",
        },
        {
            "title": "Public Relation & Communication Officer",
            "description": (
                "Managed communication and public relations initiatives for student "
                "activities at BEM Fasilkom UI."
            ),
            "category": "volunteer",
        },
        {
            "title": "Executive Board Secretary",
            "description": (
                "Handled administrative coordination, documentation, and internal "
                "communication for Arung CS UI."
            ),
            "category": "volunteer",
        },
    ]

    for award in awards:
        Award.objects.get_or_create(title=award["title"], defaults=award)

    for experience in experiences:
        Experience.objects.get_or_create(
            title=experience["title"],
            defaults=experience,
        )


def remove_initial_portfolio_data(apps, schema_editor):
    Award = apps.get_model("main", "Award")
    Experience = apps.get_model("main", "Experience")

    Award.objects.filter(
        title__in=[
            "Winner, RISTEK Hackathon 2026",
            "Best Exhibition Awardee, RISTEK Hackathon 2026",
            "Top National Finalist, Hackathon Digital Cooperatives Expo 2026",
            "Best 1st Graduation Student 2026",
        ]
    ).delete()

    Experience.objects.filter(
        title__in=[
            "Lecturer Assistant, Business Management",
            "Public Relation & Communication Officer",
            "Executive Board Secretary",
        ]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_award"),
    ]

    operations = [
        migrations.RunPython(
            create_initial_portfolio_data,
            remove_initial_portfolio_data,
        ),
    ]
