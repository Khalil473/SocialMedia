import json

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


def print_stars():
    print("***********************************************")


def pretty_responce(response):
    return json.dumps(response.data, indent=4)


def create_user(cli, email, password):
    return cli.post(
        path="/auth/sign_up/",
        data={"email": email, "password": password},
        format="json",
    )


def log_in(cli, email, password):
    return cli.post(
        path="/auth/log_in/", data={"email": email, "password": password}, format="json"
    )


class SignUpTestCase(TestCase):

    cli = APIClient()

    @classmethod
    def setUpTestData(cls):
        print_stars()
        print_stars()
        print_stars()
        print("\tSign up test cases")
        print_stars()
        print_stars()

    def setUp(self) -> None:
        print_stars()

    def test_sign_up_get(self):
        response = self.cli.get(path="/auth/sign_up/", format="json")
        print("response of sign_up get request")
        print(pretty_responce(response))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sign_up_post_weak_password(self):
        response = create_user(self.cli, "kw@gmail.com", "12345")
        print("response of sign_up post request with weak password")
        print(pretty_responce(response))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sign_up_post_strong_password(self):
        response = create_user(self.cli, "kw@gmail.com", "Aasdfasdk!@3")
        print("response of sign_up post request with strong password")
        print(pretty_responce(response))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_sign_up_post_duplicate_email(self):
        create_user(self.cli, "kw@gmail.com", "aadas2!@3")
        response = create_user(self.cli, "kw@gmail.com", "Aasdfasdk!@3")
        print("response of sign_up post request with duplicate_email")
        print(pretty_responce(response))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTestCase(TestCase):

    cli = APIClient()

    @classmethod
    def setUpTestData(cls):
        print_stars()
        print_stars()
        print_stars()
        print("\t Login test cases")
        print_stars()
        print_stars()

    def setUp(self) -> None:
        print_stars()

    def test_login_wrong_creds(self):
        response = log_in(self.cli, "aaa@aaa.com", "1234556")
        print("response of log_in post request with wrong credentials")
        print(pretty_responce(response))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_right_creds(self):
        create_user(self.cli, "aaa@aaa.com", "asdad@aamc4")
        response = log_in(self.cli, "aaa@aaa.com", "asdad@aamc4")
        print("response of log_in post request with right credentials")
        print(pretty_responce(response))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
