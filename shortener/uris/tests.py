import string

from django.test import TestCase
from rest_framework.test import APITestCase
from django.shortcuts import reverse

from uris.models import Link


class LinkModelTestCase(TestCase):
    def test_generate_short_code(self):
        short_code = Link.generate_short_code()
        self.assertEqual(len(short_code), 12)
        for character in short_code:
            self.assertIn(
                character, 
                string.ascii_lowercase+string.ascii_uppercase+string.digits
            )

    def test_short_path(self):
        short_code = Link.generate_short_code()
        link = Link.objects.create(
            target_url="https://example.com",
            short_code=short_code
        )

        path = link.short_path
        self.assertIn(short_code, link.short_path)
        self.assertTrue(path.startswith("/short/"))
        self.assertTrue(path.endswith(short_code))


class LinkViewsetTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("api:link-list")

    def test_create_shortened_url(self):
        payload = {
            "target_url": "https://docs.djangoproject.com/" 
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertRegex(data["short_url"], r"http://testserver/short/[A-Za-z0-9]{12}")

    def test_create_shortened_url_custom_short_code(self):
        payload = {
            "target_url": "https://docs.djangoproject.com/",
            "short_code": "test1"
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["short_url"], "http://testserver/short/test1")
    
    def test_create_shortened_url_custom_short_code_already_exists(self):
        payload = {
            "target_url": "https://docs.djangoproject.com/",
            "short_code": "test1"
        }
        link = Link.objects.create(**payload)

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertDictEqual(
            data,
            {'short_code': ['Short Code is already taken!']}
        )

    def test_create_shortened_url_custom_short_code_too_long(self):
        payload = {
            "target_url": "https://docs.djangoproject.com/",
            "short_code": "averylongshortcodedefinietlyttoolong"
        }

        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertDictEqual(
            data,
            {'short_code': ['Ensure this field has no more than 12 characters.']}
        )


class ShortViewTestCase(TestCase):
    def test_redirect_correct(self):
        payload = {
            "target_url": "https://docs.djangoproject.com/",
            "short_code": "test1"
        }
        Link.objects.create(**payload)
        url = reverse("short", kwargs={"short_code": "test1"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_redirect_wrong_short_code(self):
        url = reverse("short", kwargs={"short_code": "notExit"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

