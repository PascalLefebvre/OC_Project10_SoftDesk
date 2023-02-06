from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from projects.models import Project, Contributor

User = get_user_model()


class TestProjectList(APITestCase):

    fixtures = ["fixtures/db_dump.json"]
    project_list_url = reverse("project_list")
    auth_username = "barbara"
    auth_password = "secret1234"

    def setUp(self):
        post_data = {
            "username": self.auth_username,
            "password": self.auth_password,
        }
        response = self.client.post("/login/", data=post_data, format="json")
        access_token = response.data["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

    def test_user_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.project_list_url)
        self.assertEquals(response.status_code, 401)

    def test_list_projects(self):
        nb_projects = Project.objects.filter(
            contributors__user__username=self.auth_username
        ).count()
        response = self.client.get(self.project_list_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), nb_projects)

    def test_create_project(self):
        nb_contributions_before_creation = Contributor.objects.filter(
            user__username=self.auth_username
        ).count()

        post_data = {
            "title": "Test project",
            "description": "Test description",
            "type": "back-end",
        }
        response = self.client.post(
            self.project_list_url, data=post_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data["title"], post_data["title"])
        self.assertEqual(response.data["description"], post_data["description"])
        self.assertEqual(response.data["type"], post_data["type"])

        # Verify the update of the contributor table.
        nb_contributions_after_creation = Contributor.objects.filter(
            user__username=self.auth_username
        ).count()
        self.assertEqual(
            nb_contributions_after_creation, nb_contributions_before_creation + 1
        )


class TestProjectDetail(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "secret1234"
        cls.project_creator = User.objects.create_user(
            username="creator", password=cls.password
        )
        cls.project = Project.objects.create(
            title="Test project", description="Test description", type="back-end"
        )
        cls.contributor = Contributor.objects.create(
            user=cls.project_creator, project=cls.project, role="AUTHOR"
        )
        cls.project_detail_url = reverse(
            "project_detail", kwargs={"project_id": cls.project.id}
        )

    def setUp(self):
        post_data = {
            "username": self.project_creator.username,
            "password": self.password,
        }
        response = self.client.post("/login/", data=post_data, format="json")
        access_token = response.data["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

    def test_retrieve_project(self):
        response = self.client.get(self.project_detail_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.project.id)

    def test_update_project(self):
        post_data = {
            "title": "Test project",
            "description": "Test description updated",
            "type": "back-end",
        }
        response = self.client.put(
            self.project_detail_url, data=post_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], post_data["title"])
        self.assertEqual(response.data["description"], post_data["description"])
        self.assertEqual(response.data["type"], post_data["type"])

    def test_delete_project(self):
        response = self.client.delete(self.project_detail_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
