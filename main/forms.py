from django.forms import CheckboxInput, ModelForm, Select, TextInput, Textarea, URLInput

from main.models import Project, Skill

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "project_url",
            "project_image_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "project_url": "URL Proyek",
            "project_image_url": "URL Gambar Proyek",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_url": URLInput(
                attrs={
                    "placeholder": "https://github.com/kakBurhan/burhanquestv4",
                }
            ),
            "project_image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = [
            "name",
            "category",
            "proficiency",
            "description",
            "icon_url",
            "is_featured",
        ]

        labels = {
            "name": "Nama Skill / Tool",
            "category": "Kategori",
            "proficiency": "Tingkat Kemampuan",
            "description": "Deskripsi Singkat",
            "icon_url": "URL Ikon",
            "is_featured": "Skill Unggulan",
        }

        help_texts = {
            "icon_url": "Opsional. Tautan gambar logo atau ikon.",
            "is_featured": "Skill unggulan ditampilkan paling atas.",
        }

        widgets = {
            "name": TextInput(
                attrs={
                    "placeholder": "Django",
                    "maxlength": 100,
                }
            ),
            "category": Select(),
            "proficiency": Select(),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan bagaimana kamu memakainya",
                    "rows": 3,
                }
            ),
            "icon_url": URLInput(
                attrs={
                    "placeholder": "https://example.com/logo.png",
                }
            ),
            "is_featured": CheckboxInput(),
        }
