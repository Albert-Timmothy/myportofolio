import uuid
from django.db import models
from django.contrib.auth.models import User


class Award(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    organizer = models.CharField(max_length=255)
    date = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    image = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title


class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
        ('organization', 'Organization'), 
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def is_ongoing(self):
        return self.ended_at is None


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    tech_stack = models.CharField(max_length=255)
    project_url = models.URLField(blank=True)
    project_image_url = models.URLField(blank=True, max_length=500)
    starred_by = models.ManyToManyField(
        User, related_name="starred_projects", blank=True
    )

    def __str__(self):
        return self.title


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('programming', 'Programming Language'),
        ('framework', 'Framework & Library'),
        ('database', 'Database'),
        ('tool', 'Tool & Platform'),
        ('design', 'Design & Creative'),
        ('business', 'Business & Strategy'),
        ('soft-skill', 'Soft Skill'),
    ]
    PROFICIENCY_CHOICES = [
        (1, '1 - Beginner'),
        (2, '2 - Basic'),
        (3, '3 - Intermediate'),
        (4, '4 - Advanced'),
        (5, '5 - Expert'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='programming')
    proficiency = models.PositiveSmallIntegerField(choices=PROFICIENCY_CHOICES, default=3)
    description = models.TextField(blank=True)
    icon_url = models.URLField(blank=True, max_length=500)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-proficiency', 'name']

    def __str__(self):
        return self.name

    @property
    def proficiency_stars(self):
        """Level keahlian dalam bentuk bintang, contoh: 4 -> ****-."""
        return '\u2605' * self.proficiency + '\u2606' * (5 - self.proficiency)