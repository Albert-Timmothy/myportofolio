from django.contrib.auth.models import Group, Permission, User
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

import json
import uuid

from main.models import Award, Experience, Project, Skill


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
        # Sejak Tugas 4, create/update/delete Skill hanya untuk yang berhak.
        self.owner = User.objects.create_superuser("owner", password="pw-owner-123")
        self.client.force_login(self.owner)
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

    def test_skills_page_renders_shell_without_database_items(self):
        response = self.client.get(reverse("main:show_skills"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skills.html")
        self.assertTemplateUsed(response, "base.html")
        self.assertNotContains(response, self.skill.description)
        self.assertNotIn("skill_list", response.context)
        self.assertContains(response, 'id="skills-grid"')
        self.assertContains(response, 'src="/static/js/skills.js"')
        self.assertContains(response, 'id="skill-form"')

    def test_empty_skills_page(self):
        Skill.objects.all().delete()
        response = self.client.get(reverse("main:show_skills"))

        self.assertContains(response, "Belum ada skill yang ditambahkan.")

    def test_skills_page_filter(self):
        Skill.objects.create(name="Figma", category="design", proficiency=3)
        response = self.client.get(reverse("main:show_skills"), {"category": "design"})

        self.assertNotContains(response, "Figma</h2>")
        self.assertContains(response, 'value="design" selected')
        self.assertNotContains(response, "Framework web berbasis Python.")

        response = self.client.get(reverse("main:show_skills"), {"name": "tidak-ada"})
        self.assertContains(response, 'value="tidak-ada"')

    def test_skills_json(self):
        response = self.client.get(reverse("main:get_skills_json"))
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["fields"]["star_count"], 0)
        self.assertFalse(data[0]["fields"]["is_starred"])
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


# ---------- Tugas 4: autentikasi, otorisasi, dan star ----------

def make_editor_group():
    """Grup Editor: hanya boleh mengubah (change) Project dan Skill."""
    group, _ = Group.objects.get_or_create(name="Editor")
    group.permissions.add(
        *Permission.objects.filter(codename__in=["change_project", "change_skill"])
    )
    return group


class RoleTestBase(TestCase):
    """Menyiapkan satu data per model dan akun untuk tiap peran."""

    def setUp(self):
        self.project = Project.objects.create(
            title="Portfolio", description="Situs pribadi", tech_stack="Django"
        )
        self.skill = Skill.objects.create(name="Django")
        self.regular = User.objects.create_user("biasa", password="pw-biasa-123")
        self.editor = User.objects.create_user("editor", password="pw-editor-123")
        self.editor.groups.add(make_editor_group())
        self.owner = User.objects.create_superuser("owner", password="pw-owner-123")

    def login_as(self, user):
        self.client.logout()
        if user is not None:
            self.client.force_login(user)

    def new_project(self):
        return Project.objects.create(title="Baru", description="d", tech_stack="t")

    def new_skill(self):
        return Skill.objects.create(name="Baru")


class RoleAccessTest(RoleTestBase):
    def test_anonymous_is_redirected_to_login(self):
        requests = [
            ("get", reverse("main:create_project")),
            ("get", reverse("main:update_project", args=[self.project.id])),
            ("post", reverse("main:delete_project", args=[self.project.id])),
            ("post", reverse("main:toggle_star", args=[self.project.id])),
            ("get", reverse("main:create_skill")),
            ("get", reverse("main:update_skill", args=[self.skill.id])),
            ("post", reverse("main:delete_skill", args=[self.skill.id])),
            ("post", reverse("main:toggle_skill_star", args=[self.skill.id])),
        ]
        for method, url in requests:
            with self.subTest(method=method, url=url):
                response = getattr(self.client, method)(url)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response["Location"].startswith("/login/"))
        self.assertTrue(Project.objects.filter(pk=self.project.id).exists())
        self.assertTrue(Skill.objects.filter(pk=self.skill.id).exists())

    def test_regular_user_gets_403_on_every_write_action(self):
        self.login_as(self.regular)
        requests = [
            ("get", reverse("main:create_project")),
            ("get", reverse("main:update_project", args=[self.project.id])),
            ("post", reverse("main:delete_project", args=[self.project.id])),
            ("get", reverse("main:create_skill")),
            ("get", reverse("main:update_skill", args=[self.skill.id])),
            ("post", reverse("main:delete_skill", args=[self.skill.id])),
        ]
        for method, url in requests:
            with self.subTest(method=method, url=url):
                self.assertEqual(getattr(self.client, method)(url).status_code, 403)
        self.assertTrue(Project.objects.filter(pk=self.project.id).exists())
        self.assertTrue(Skill.objects.filter(pk=self.skill.id).exists())

    def test_editor_can_update_but_not_create_or_delete(self):
        self.login_as(self.editor)

        self.assertEqual(
            self.client.get(reverse("main:update_project", args=[self.project.id])).status_code, 200
        )
        self.assertEqual(
            self.client.get(reverse("main:update_skill", args=[self.skill.id])).status_code, 200
        )
        self.assertEqual(self.client.get(reverse("main:create_project")).status_code, 403)
        self.assertEqual(self.client.get(reverse("main:create_skill")).status_code, 403)
        self.assertEqual(
            self.client.post(reverse("main:delete_project", args=[self.project.id])).status_code, 403
        )
        self.assertEqual(
            self.client.post(reverse("main:delete_skill", args=[self.skill.id])).status_code, 403
        )

    def test_editor_update_is_saved(self):
        self.login_as(self.editor)
        response = self.client.post(
            reverse("main:update_project", args=[self.project.id]),
            {"title": "Diubah Editor", "description": "d", "tech_stack": "Django"},
        )

        self.assertRedirects(response, reverse("main:show_projects"))
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Diubah Editor")

    def test_owner_has_full_access(self):
        self.login_as(self.owner)

        self.assertEqual(self.client.get(reverse("main:create_project")).status_code, 200)
        self.assertEqual(self.client.get(reverse("main:create_skill")).status_code, 200)
        self.assertEqual(
            self.client.get(reverse("main:update_project", args=[self.project.id])).status_code, 200
        )

        project, skill = self.new_project(), self.new_skill()
        self.client.post(reverse("main:delete_project", args=[project.id]))
        self.client.post(reverse("main:delete_skill", args=[skill.id]))
        self.assertFalse(Project.objects.filter(pk=project.id).exists())
        self.assertFalse(Skill.objects.filter(pk=skill.id).exists())


class ButtonVisibilityTest(RoleTestBase):
    """Tombol aksi hanya tampil untuk yang berhak (server tetap memeriksa)."""

    def page(self, user, name):
        self.login_as(user)
        return self.client.get(reverse(name)).content.decode()

    def test_projects_page_buttons_per_role(self):
        cases = [
            (None, False, False, False),
            (self.regular, False, False, False),
            (self.editor, False, True, False),
            (self.owner, True, True, True),
        ]
        for user, can_add, can_edit, can_delete in cases:
            with self.subTest(user=user):
                html = self.page(user, "main:show_projects")
                self.assertEqual("Tambah Proyek" in html, can_add)
                self.assertIn(f'const CAN_EDIT = "{str(can_edit).lower()}"', html)
                self.assertIn(f'const CAN_DELETE = "{str(can_delete).lower()}"', html)
                self.assertEqual('id="project-form"' in html, can_add)

    def test_skills_page_buttons_per_role(self):
        cases = [
            (None, False, False, False),
            (self.regular, False, False, False),
            (self.editor, False, True, False),
            (self.owner, True, True, True),
        ]
        for user, can_add, can_edit, can_delete in cases:
            with self.subTest(user=user):
                html = self.page(user, "main:show_skills")
                self.assertEqual("Tambah Skill" in html, can_add)
                self.assertIn(f'data-can-edit="{str(can_edit).lower()}"', html)
                self.assertEqual('id="delete-skill-modal"' in html, can_delete)
                self.assertEqual('id="skill-form"' in html, can_add)


class StarTest(RoleTestBase):
    def test_toggle_star_adds_then_removes_for_both_models(self):
        cases = [
            (self.project, "main:toggle_star"),
            (self.skill, "main:toggle_skill_star"),
        ]
        for item, url_name in cases:
            with self.subTest(url=url_name):
                self.login_as(self.regular)
                url = reverse(url_name, args=[item.id])

                self.client.post(url)
                self.assertEqual(item.starred_by.count(), 1)
                self.assertIn(self.regular, item.starred_by.all())

                self.client.post(url)
                self.assertEqual(item.starred_by.count(), 0)

    def test_star_is_limited_to_one_per_user(self):
        url = reverse("main:toggle_star", args=[self.project.id])
        self.login_as(self.regular)
        self.client.post(url)
        self.login_as(self.editor)
        self.client.post(url)

        self.assertEqual(self.project.starred_by.count(), 2)

    def test_star_rejects_get(self):
        self.login_as(self.regular)
        for name, item in (("main:toggle_star", self.project), ("main:toggle_skill_star", self.skill)):
            with self.subTest(url=name):
                response = self.client.get(reverse(name, args=[item.id]))
                self.assertEqual(response.status_code, 405)
                self.assertEqual(item.starred_by.count(), 0)

    def test_star_count_and_state_are_shown(self):
        self.project.starred_by.add(self.regular)

        # Halaman hanya kerangka; star dibaca dari JSON sesuai pengguna yang login.
        self.login_as(self.regular)
        data = json.loads(self.client.get(reverse("main:get_projects_json")).content)
        self.assertEqual(data[0]["fields"]["star_count"], 1)
        self.assertTrue(data[0]["fields"]["is_starred"])

        self.login_as(None)
        data = json.loads(self.client.get(reverse("main:get_projects_json")).content)
        self.assertEqual(data[0]["fields"]["star_count"], 1)
        self.assertFalse(data[0]["fields"]["is_starred"])


class JsonPrivacyTest(RoleTestBase):
    def test_json_does_not_leak_who_starred(self):
        self.project.starred_by.add(self.regular)
        self.skill.starred_by.add(self.regular)

        for name in ("main:get_projects_json", "main:get_skills_json"):
            with self.subTest(url=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)
                self.assertNotContains(response, "starred_by")
                self.assertNotContains(response, "biasa")

    def test_projects_json_still_has_project_data(self):
        data = json.loads(self.client.get(reverse("main:get_projects_json")).content)

        self.assertEqual(data[0]["fields"]["title"], "Portfolio")
        self.assertEqual(data[0]["fields"]["tech_stack"], "Django")


class SkillAjaxTest(RoleTestBase):
    def setUp(self):
        super().setUp()
        self.url = reverse("main:create_skill_ajax")
        self.data = {
            "name": "<b>Flutter</b>",
            "category": "framework",
            "proficiency": 3,
            "description": '<img src="x" onerror="alert(1)">Mobile apps',
        }

    def test_only_owner_can_create_through_ajax(self):
        for user in (None, self.regular, self.editor):
            with self.subTest(user=user):
                self.login_as(user)
                response = self.client.post(self.url, self.data)
                self.assertEqual(response.status_code, 403)
                self.assertIn("message", response.json())
        self.assertFalse(Skill.objects.filter(name="Flutter").exists())

        self.login_as(self.owner)
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, 201)
        skill = Skill.objects.get(pk=response.json()["pk"])
        self.assertEqual(skill.name, "Flutter")
        self.assertEqual(skill.description, "Mobile apps")

    def test_invalid_input_returns_errors_without_saving(self):
        self.login_as(self.owner)
        before = Skill.objects.count()
        for invalid in ({"name": '<img src="x" onerror="alert(1)">'},
                        {"proficiency": 9}, {"category": "unknown"},
                        {"icon_url": "javascript:alert(1)"}):
            with self.subTest(invalid=invalid):
                response = self.client.post(self.url, {**self.data, **invalid})
                self.assertEqual(response.status_code, 400)
                self.assertIn(next(iter(invalid)), response.json()["errors"])
        self.assertEqual(Skill.objects.count(), before)

    def test_ajax_requires_post_and_csrf(self):
        self.login_as(self.owner)
        self.assertEqual(self.client.get(self.url).status_code, 405)
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.owner)
        self.assertEqual(csrf_client.post(self.url, self.data).status_code, 403)
        csrf_client.get(reverse("main:create_skill"))
        token = csrf_client.cookies["csrftoken"].value
        response = csrf_client.post(self.url, self.data, HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, 201)

    def test_json_star_state_filters_and_privacy(self):
        self.skill.starred_by.add(self.regular)
        Skill.objects.create(name="Figma", category="design")
        url = reverse("main:get_skills_json")
        for user, expected in ((None, False), (self.regular, True), (self.editor, False)):
            with self.subTest(user=user):
                self.login_as(user)
                response = self.client.get(url, {"name": "dJaNgO", "category": "programming"})
                data = response.json()
                self.assertEqual(len(data), 1)
                fields = data[0]["fields"]
                self.assertEqual(fields["star_count"], 1)
                self.assertEqual(fields["is_starred"], expected)
                self.assertNotContains(response, self.regular.username)
                self.assertNotIn("starred_by", fields)
        self.assertEqual(self.client.get(url, {"name": "missing"}).json(), [])