import uuid

from django.contrib.auth.models import Group, Permission, User
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase

from main.models import Skill


class SkillAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_superuser("skill-owner", password="test-password")
        cls.visitor = User.objects.create_user("skill-visitor", password="test-password")
        cls.editor = User.objects.create_user("skill-editor", password="test-password")
        group, _ = Group.objects.get_or_create(name="Editor")
        group.permissions.add(Permission.objects.get(content_type__app_label="main", codename="change_skill"))
        cls.editor.groups.add(group)
        cls.skill = Skill.objects.create(name="Django", category="framework", proficiency=3)

    def setUp(self):
        self.list_url = reverse("api:skill-list")
        self.detail_url = reverse("api:skill-detail", args=[self.skill.pk])
        self.star_url = reverse("api:skill-star", args=[self.skill.pk])
        self.payload = {"name": "Python", "category": "programming", "proficiency": 4}

    def test_public_read_filter_and_missing(self):
        response = self.client.get(self.list_url, {"name": "DJAN", "category": "framework"})
        self.assertEqual(response.status_code, 200)
        self.assertIn(str(self.skill.pk), [item["id"] for item in response.data])
        self.assertEqual(self.client.get(self.list_url, {"name": "missing-xyz"}).data, [])
        detail = self.client.get(self.detail_url)
        self.assertEqual(detail.status_code, 200)
        self.assertEqual(detail.data["category_display"], "Framework & Library")
        self.assertEqual(self.client.get(reverse("api:skill-detail", args=[uuid.uuid4()])).status_code, 404)

    def test_guest_and_regular_cannot_write(self):
        before = Skill.objects.count()
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            for method in ("put", "patch"):
                self.assertEqual(getattr(self.client, method)(self.detail_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Skill.objects.count(), before)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.name, "Django")

    def test_editor_can_update_but_cannot_create_delete(self):
        self.client.force_authenticate(user=self.editor)
        self.assertEqual(self.client.patch(self.detail_url, {"proficiency": 5}, format="json").status_code, 200)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.proficiency, 5)
        self.assertEqual(self.skill.name, "Django")
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 200)
        before = list(Skill.objects.order_by("pk").values())
        self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
        self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(list(Skill.objects.order_by("pk").values()), before)
        self.assertEqual(self.client.options(self.detail_url).status_code, 200)
        self.assertTrue(Skill.objects.filter(pk=self.skill.pk).exists())

    def test_owner_crud_and_read_only_fields(self):
        self.client.force_authenticate(user=self.owner)
        forged_id = str(uuid.uuid4())
        response = self.client.post(self.list_url, {
            **self.payload, "id": forged_id, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.pk],
        }, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertNotEqual(response.data["id"], forged_id)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["starred_by_names"], "")
        self.assertEqual(self.client.patch(self.detail_url, {"name": "Updated"}, format="json").status_code, 200)
        self.assertEqual(self.client.put(self.detail_url, {"description": "Missing name"}, format="json").status_code, 400)
        self.assertEqual(self.client.put(self.detail_url, self.payload, format="json").status_code, 200)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.content, b"")
        self.assertFalse(Skill.objects.filter(pk=self.skill.pk).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        before = Skill.objects.count()
        for changes, field in [
            ({"name": " "}, "name"), ({"name": "<b></b>"}, "name"),
            ({"category": "invalid"}, "category"), ({"proficiency": 6}, "proficiency"),
            ({"icon_url": "javascript:alert(1)"}, "icon_url"),
        ]:
            with self.subTest(changes=changes):
                response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
                self.assertEqual(response.status_code, 400)
                self.assertIn(field, response.data)
        self.assertEqual(Skill.objects.count(), before)

    def test_star_identity_toggle_and_methods(self):
        self.assertEqual(self.client.post(self.star_url).status_code, 403)
        self.assertFalse(self.skill.starred_by.exists())
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["star_count"], 1)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["starred_by_names"], self.visitor.username)
        self.assertNotIn("email", response.data)
        self.assertNotIn("password", response.data)
        self.assertTrue(self.skill.starred_by.filter(pk=self.visitor.pk).exists())
        self.assertEqual(self.client.post(self.star_url).data["star_count"], 0)
        self.assertEqual(self.client.get(self.star_url).status_code, 405)
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, 405)

    def test_legacy_create_delete_do_not_bypass_owner_requirement(self):
        self.editor.user_permissions.add(*Permission.objects.filter(
            content_type__app_label="main", codename__in=["add_skill", "delete_skill"],
        ))
        self.client.force_login(self.editor)
        before = list(Skill.objects.order_by("pk").values())
        for name, args in [
            ("main:create_skill", []), ("main:create_skill_ajax", []),
            ("main:delete_skill", [self.skill.pk]),
        ]:
            with self.subTest(view=name):
                response = self.client.post(reverse(name, args=args), self.payload)
                self.assertEqual(response.status_code, 403)
                self.assertEqual(list(Skill.objects.order_by("pk").values()), before)

    def test_edit_page_and_session_patch_for_editor_and_owner(self):
        for user in (self.editor, self.owner):
            with self.subTest(user=user.username):
                client = APIClient(enforce_csrf_checks=True)
                self.assertTrue(client.login(username=user.username, password="test-password"))
                page = client.get(reverse("main:update_skill", args=[self.skill.pk]))
                self.assertContains(page, f'data-api-url="{self.detail_url}"')
                self.assertContains(page, 'js/skill_edit.js')
                before = Skill.objects.get(pk=self.skill.pk).name
                response = client.patch(self.detail_url, {"name": "Ditolak"}, format="json")
                self.assertEqual(response.status_code, 403)
                self.skill.refresh_from_db()
                self.assertEqual(self.skill.name, before)
                token = client.cookies["csrftoken"].value
                response = client.patch(self.detail_url, {"name": "<b>Python</b>"},
                                        format="json", HTTP_X_CSRFTOKEN=token)
                self.assertEqual(response.status_code, 200)
                self.skill.refresh_from_db()
                self.assertEqual(self.skill.name, "Python")

    def test_star_uses_session_user_and_requires_csrf_for_each_role(self):
        for user in (self.visitor, self.editor, self.owner):
            with self.subTest(user=user.username):
                client = APIClient(enforce_csrf_checks=True)
                self.assertTrue(client.login(username=user.username, password="test-password"))
                client.get(reverse("main:show_skills"))
                before = self.skill.starred_by.count()
                self.assertEqual(client.post(self.star_url).status_code, 403)
                self.assertEqual(self.skill.starred_by.count(), before)
                token = client.cookies["csrftoken"].value
                response = client.post(self.star_url, {"user_id": self.owner.pk},
                                       format="json", HTTP_X_CSRFTOKEN=token)
                self.assertEqual(response.status_code, 200)
                self.assertTrue(self.skill.starred_by.filter(pk=user.pk).exists())
                self.assertEqual(self.skill.starred_by.count(), before + 1)

    def test_session_csrf_and_frontend_routes(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="skill-owner", password="test-password"))
        self.assertEqual(client.post(self.list_url, self.payload, format="json").status_code, 403)
        page = client.get(reverse("main:show_skills"))
        self.assertContains(page, self.list_url)
        self.assertContains(page, '/api/v1/skills/00000000-0000-0000-0000-000000000000/star/')
        token = client.cookies["csrftoken"].value
        self.assertEqual(client.post(self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token).status_code, 201)
