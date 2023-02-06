from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class TestContributorList(APITestCase):

    fixtures = ["fixtures/db_dump.json"]
    contributor_list_url = reverse("contributor_list", kwargs={"project_id": 2})
    # "barbara" is a contributor of the project '2'
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

    def test_create_contributor_if_auth_user_is_not_project_author(self):
        post_data = {
            "user": self.new_user.id,
            "role": "CONTRIBUTOR",
        }
        response = self.client.post(
            self.contributor_list_url, data=post_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()["detail"],
            "You do not have permission to perform this action.",
        )


class TestContributorDelete(APITestCase):
    pass
