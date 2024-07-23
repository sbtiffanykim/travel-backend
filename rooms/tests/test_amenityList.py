from rest_framework.test import APITestCase
from rooms import models


class TestAmenityList(APITestCase):

    NAME = "Amenity Test"
    DESCRIPTION = "Amenity Description"

    URL = "/api/v1/rooms/amenities/"

    def setUp(self):
        models.Amenity.objects.create(name=self.NAME, description=self.DESCRIPTION)

    def test_all_amenities(self):
        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Public access check failed: Expected status code 200 but got {response.status_code}",
        )
        self.assertEqual(
            data["page"]["count"],
            1,
            f"",
        )
        self.assertEqual(
            data["content"][0]["name"],
            self.NAME,
            f'Amenity name mismatch: Expected {self.NAME} but got {data["content"][0]["name"]}',
        )
        self.assertEqual(
            data["content"][0]["description"],
            self.DESCRIPTION,
            f'Amenity description mismatch: Expected {self.DESCRIPTION} but got {data["content"][0]["description"]}',
        )

    def test_create_amenity_success(self):

        new_amenity_name = "New Amenity"
        new_amenity_description = "New Amenity Description"

        response = self.client.post(self.URL, data={"name": new_amenity_name, "description": new_amenity_description})
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Public access check failed: Expected status code 200 but got {response.status_code}",
        )
        self.assertEqual(data["name"], new_amenity_name)
        self.assertEqual(data["description"], new_amenity_description)

    def test_create_amenity_missing_name(self):
        response = self.client.post(self.URL)
        error_data = response.json()

        self.assertEqual(
            response.status_code,
            400,
            f"Public access check failed: Expected status code 400 but got {response.status_code}",
        )
        self.assertIn("name", error_data)
