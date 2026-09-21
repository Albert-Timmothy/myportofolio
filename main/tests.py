from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

import json
import uuid

from main.models import Award, Experience, Skill


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )
        self.award = Award.objects.create(
            title="Juara 1 Hackathon",
            organizer="Fasilkom UI",
            date="Sep 2026",
            description="Membuat solusi digital berbasis web.",
            image="img/winnerristekhackathon.png",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, self.experience.title)
        self.assertContains(response, "Selesai")

    def test_award_model(self):
        self.assertEqual(str(self.award), "Juara 1 Hackathon")
        self.assertEqual(self.award.organizer, "Fasilkom UI")

    def test_award_page(self):
        response = self.client.get(reverse("main:show_award"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "award.html")
        self.assertContains(response, self.award.title)
        self.assertContains(response, self.award.organizer)
        self.assertContains(response, self.award.date)
        self.assertContains(response, self.award.description)
        self.assertContains(response, self.award.image)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_empty_award_page(self):
        Award.objects.all().delete()
        response = self.client.get(reverse("main:show_award"))

        self.assertContains(response, "Belum ada award yang ditambahkan.")


class SkillTest(TestCase):
    def setUp(self):
        self.skill = Skill.objects.create(
            name="Django",
            category="framework",
            proficiency=4,
            description="Framework web berbasis Python.",
            icon_url="https://example.com/django.png",
            is_featured=True,
        )
        self.valid_data = {
            "name": "Flutter",
            "category": "framework",
            "proficiency": 3,
            "description": "Membangun aplikasi mobile.",
            "icon_url": "https://example.com/flutter.png",
            "is_featured": "on",
        }

    def test_skill_model(self):
        self.assertEqual(str(self.skill), "Django")
        self.assertEqual(self.skill.proficiency_stars, "\u2605" * 4 + "\u2606")
        self.assertEqual(self.skill.get_category_display(), "Framework & Library")

    def test_skills_page_uses_base_and_shows_data(self):
        response = self.client.get(reverse("main:show_skills"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skills.html")
        self.assertTemplateUsed(response, "base.html")
        self.assertContains(response, "Django")
        self.assertContains(response, "Framework &amp; Library")
        self.assertContains(response, "4 - Advanced")
        self.assertContains(response, reverse("main:update_skill", args=[self.skill.id]))
        self.assertContains(response, reverse("main:delete_skill", args=[self.skill.id]))

    def test_empty_skills_page(self):
        Skill.objects.all().delete()
        response = self.client.get(reverse("main:show_skills"))

        self.assertContains(response, "Belum ada skill yang ditambahkan.")

    def test_skills_page_filter(self):
        Skill.objects.create(name="Figma", category="design", proficiency=3)
        response = self.client.get(reverse("main:show_skills"), {"category": "design"})

        self.assertContains(response, "Figma")
        self.assertNotContains(response, "Framework web berbasis Python.")

        response = self.client.get(reverse("main:show_skills"), {"name": "tidak-ada"})
        self.assertContains(response, "Tidak ada skill yang cocok dengan filter tersebut.")

    def test_skills_json(self):
        response = self.client.get(reverse("main:get_skills_json"))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["model"], "main.skill")
        self.assertEqual(data[0]["pk"], str(self.skill.id))
        self.assertEqual(data[0]["fields"]["name"], "Django")
        self.assertEqual(data[0]["fields"]["proficiency"], 4)
        self.assertTrue(data[0]["fields"]["is_featured"])

    def test_skills_json_filter(self):
        Skill.objects.create(name="Figma", category="design", proficiency=3)
        data = json.loads(self.client.get(reverse("main:get_skills_json"), {"name": "fig"}).content)

        self.assertEqual([item["fields"]["name"] for item in data], ["Figma"])

    def test_create_skill_form_page(self):
        response = self.client.get(reverse("main:create_skill"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skill_form.html")
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_create_skill(self):
        response = self.client.post(reverse("main:create_skill"), self.valid_data)

        self.assertRedirects(response, reverse("main:show_skills"))
        skill = Skill.objects.get(name="Flutter")
        self.assertEqual(skill.proficiency, 3)
        self.assertTrue(skill.is_featured)

    def test_create_skill_invalid(self):
        data = {**self.valid_data, "name": "", "icon_url": "bukan-url"}
        response = self.client.post(reverse("main:create_skill"), data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Skill.objects.count(), 1)
        self.assertContains(response, "form-error")

    def test_update_skill_page_is_prefilled(self):
        response = self.client.get(reverse("main:update_skill", args=[self.skill.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skill_form.html")
        self.assertContains(response, 'value="Django"')

    def test_update_skill(self):
        url = reverse("main:update_skill", args=[self.skill.id])
        data = {**self.valid_data, "name": "Django REST", "proficiency": 5}
        response = self.client.post(url, data)

        self.assertRedirects(response, reverse("main:show_skills"))
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.name, "Django REST")
        self.assertEqual(self.skill.proficiency, 5)
        self.assertEqual(Skill.objects.count(), 1)

    def test_update_skill_invalid_keeps_old_data(self):
        url = reverse("main:update_skill", args=[self.skill.id])
        response = self.client.post(url, {**self.valid_data, "name": ""})

        self.assertEqual(response.status_code, 200)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.name, "Django")

    def test_update_unknown_skill_returns_404(self):
        response = self.client.get(reverse("main:update_skill", args=[uuid.uuid4()]))

        self.assertEqual(response.status_code, 404)

    def test_delete_skill(self):
        response = self.client.post(reverse("main:delete_skill", args=[self.skill.id]))

        self.assertRedirects(response, reverse("main:show_skills"))
        self.assertFalse(Skill.objects.filter(pk=self.skill.id).exists())

    def test_delete_skill_rejects_get(self):
        response = self.client.get(reverse("main:delete_skill", args=[self.skill.id]))

        self.assertEqual(response.status_code, 405)
        self.assertTrue(Skill.objects.filter(pk=self.skill.id).exists())


class NavbarAndJsonTest(TestCase):
    def test_every_page_shares_navbar_from_base(self):
        for name in ("show_main", "show_award", "show_experience", "show_projects", "show_skills"):
            with self.subTest(page=name):
                response = self.client.get(reverse(f"main:{name}"))

                self.assertTemplateUsed(response, "base.html")
                self.assertContains(response, reverse("main:show_projects"))
                self.assertContains(response, reverse("main:show_skills"))

    def test_award_and_experience_json(self):
        Award.objects.create(title="Juara 1", organizer="Fasilkom UI", date="Sep 2026")
        Experience.objects.create(title="Asdos", description="Membantu mahasiswa.")

        awards = json.loads(self.client.get(reverse("main:get_awards_json")).content)
        experiences = json.loads(self.client.get(reverse("main:get_experiences_json")).content)

        self.assertIn("Juara 1", [item["fields"]["title"] for item in awards])
        self.assertIn("Asdos", [item["fields"]["title"] for item in experiences])
