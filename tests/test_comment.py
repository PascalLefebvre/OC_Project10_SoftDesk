from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class TestCommentList(APITestCase):
    pass


class TestProjectDetail(APITestCase):

    fixtures = ["fixtures/db_dump.json"]
    comment_detail_url = reverse(
        "comment_detail",
        kwargs={"project_id": 1, "issue_id": 3, "comment_id": 1},
    )
    # "barbara" (id '2') is the author of the issue '3' and comment "1".
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

    def test_retrieve_project(self):
        response = self.client.get(self.comment_detail_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], 1)
        self.assertEqual(response.data["description"], "Description of the comment 1")
        self.assertEqual(response.data["author"], 2)
        self.assertEqual(response.data["issue"], 3)
