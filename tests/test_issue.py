from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class TestIssueList(APITestCase):

    fixtures = ["fixtures/db_dump.json"]
    issue_list_url = reverse("issue_list", kwargs={"project_id": 1})
    # "barbara" is the author of the project '1'
    auth_username = "barbara"
    auth_password = "secret1234"

    @classmethod
    def setUpTestData(cls):
        cls.password = "secret1234"
        cls.new_user = User.objects.create_user(
            username="newuser", password=cls.password
        )

    def setUp(self):
        post_data = {
            "username": self.auth_username,
            "password": self.auth_password,
        }
        response = self.client.post("/login/", data=post_data, format="json")
        access_token = response.data["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

    def test_create_issue_if_assignee_is_not_project_contributor(self):
        post_data = {
            "title": "New issue",
            "description": "Description of the new issue",
            "tag": "bug",
            "priority": "ELEVEE",
            "status": "ENCOURS",
            "assignee": self.new_user.id,
        }
        response = self.client.post(self.issue_list_url, data=post_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()["creation denied"],
            "The assignee of the issue must be a contributor of the project.",
        )


class TestIssueDetail(APITestCase):
    pass
