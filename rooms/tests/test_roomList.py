from rest_framework.test import APITestCase
from rooms import models
from users.models import User
from categories.models import Category


class TestRoomList(APITestCase):

    URL = "/api/v1/rooms/"

    def setUp(self):
        self.user = User.objects.create(username="test")
        self.category = Category.objects.create(name="Test Category", kind=Category.CategoryKindChoices.ROOMS)
        self.amenity = models.Amenity.objects.create(name="Test Amenity")

    def test_create_room_without_authentication(self):

        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, 403)

    def test_create_room_with_missing_fields(self):

        self.client.force_login(self.user)

        response = self.client.post(self.URL)
        data = response.json()
        expected_errors = {
            "name": ["This field is required."],
            "price": ["This field is required."],
            "number_of_rooms": ["This field is required."],
            "bathrooms": ["This field is required."],
            "description": ["This field is required."],
            "address": ["This field is required."],
            "room_type": ["This field is required."],
        }

        self.assertEqual(response.status_code, 400)
        self.assertDictEqual(data, expected_errors)
