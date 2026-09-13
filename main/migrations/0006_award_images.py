from django.db import migrations


AWARD_IMAGES = {
    "Winner, RISTEK Hackathon 2026": "img/winnerristekhackathon.png",
    "Best Exhibition Awardee, RISTEK Hackathon 2026": "img/bestexhibitionawardee.png",
    "Top National Finalist, Hackathon Digital Cooperatives Expo 2026": "img/sertifikatsimkopdes-1.png",
    "Best 1st Graduation Student 2026": "img/sertifikatrangking1.png",
}


def add_award_images(apps, schema_editor):
    Award = apps.get_model("main", "Award")

    for title, image in AWARD_IMAGES.items():
        Award.objects.filter(title=title).update(image=image)


def remove_award_images(apps, schema_editor):
    Award = apps.get_model("main", "Award")

    Award.objects.filter(title__in=AWARD_IMAGES.keys()).update(image="")


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_award_image"),
    ]

    operations = [
        migrations.RunPython(add_award_images, remove_award_images),
    ]
