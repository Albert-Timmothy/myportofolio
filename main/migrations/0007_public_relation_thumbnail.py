from django.db import migrations


def set_public_relation_thumbnail(apps, schema_editor):
    Experience = apps.get_model("main", "Experience")

    Experience.objects.filter(
        title="Public Relation & Communication Officer"
    ).update(thumbnail="img/bemfasilkomui.png")


def unset_public_relation_thumbnail(apps, schema_editor):
    Experience = apps.get_model("main", "Experience")

    Experience.objects.filter(
        title="Public Relation & Communication Officer"
    ).update(thumbnail="")


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0006_award_images"),
    ]

    operations = [
        migrations.RunPython(
            set_public_relation_thumbnail,
            unset_public_relation_thumbnail,
        ),
    ]
