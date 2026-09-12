

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Award',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('organizer', models.CharField(max_length=255)),
                ('date', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
            ],
        ),
    ]
