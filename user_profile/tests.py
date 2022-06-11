from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from user_auth.tests import create_user, log_in, pretty_responce, print_stars

# Create your tests here.


def setup_token(cli):
    email = "khalil@gmail.com"
    password = "AS3@dsadw475"
    create_user(cli, email=email, password=password)
    token_response = log_in(cli, email, password)
    token = token_response.data.get("token")
    cli.credentials(HTTP_AUTHORIZATION="Token " + token)


class MyProfileTestCase(TestCase):
    cli = APIClient()
    path = "/profiles/my_profile/"

    @classmethod
    def setUpTestData(cls):
        print_stars()
        print_stars()
        print_stars()
        print("\tMy Profile test cases")
        print_stars()
        print_stars()

    def setUp(self) -> None:
        self.cli.credentials()
        print_stars()

    def test_get_profile_with_token(self):
        setup_token(self.cli)
        response = self.cli.get(path=self.path, format="json")
        print("response of my profile get request")
        print(pretty_responce(response))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_profile_without_token(self):
        response = self.cli.get(path=self.path, format="json")
        print("response of my profile without token get request")
        print(pretty_responce(response))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_my_profile(self):
        setup_token(self.cli)
        response = self.cli.patch(
            path=self.path,
            format="json",
            data={"bio": "bio_from_test", "location": "location from test"},
        )
        print("response of my profile bio update patch request")
        response1 = self.cli.get(path=self.path, format="json")
        print(pretty_responce(response1))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ProfileSearch(TestCase):
    cli = APIClient()
    path = "/profiles/search/"

    @classmethod
    def setUpTestData(cls):
        print_stars()
        print_stars()
        print_stars()
        print("\tSearch Profiles test cases")
        print_stars()
        print_stars()
        print("crearing demo users")
        password = "asd@asdas21321"
        for i in range(20):
            email = "test" + str(i) + "@gmail.com"
            first_name = "first " + str(i % 8)
            last_name = "last " + str((i + 1) % 3)
            create_user(
                cli=cls.cli,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
        setup_token(cls.cli)

    def search_profiles(self, data=None):
        return self.cli.get(path=self.path, data=data)

    def setUp(self) -> None:
        print_stars()

    def test_search_no_params(self):
        response = self.search_profiles()
        print("response of searching without params get request")
        print(pretty_responce(response))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_with_email(self):
        response = self.search_profiles(data={"email": "test5@gmail.com"})
        print("response of searching via email get request")
        print(pretty_responce(response))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_with_first_name(self):
        response = self.search_profiles(data={"first_name": "first 2"})
        print("response of searching via first name get request")
        print(pretty_responce(response))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_with_multiple_params(self):
        response = self.search_profiles(
            data={"first_name": "first 2", "last_name": "last 0"}
        )
        print("response of searching via multiple params get request")
        print(pretty_responce(response))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
