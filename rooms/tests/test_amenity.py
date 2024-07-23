from rest_framework.test import APITestCase
from rooms import models


class TestAmenityDetail(APITestCase):

    NAME = "Test Amenity Name"
    DESCRIPTION = "Test Amenity Description"

    URL = "/api/v1/rooms/amenities"

    def setUp(self):
        models.Amenity.objects.create(name=self.NAME, description=self.DESCRIPTION)

    def test_get_amenity_success(self):
        response = self.client.get(f"{self.URL}/1")
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            f"Public access check failed: Expected status code 200 but got {response.status_code}",
        )
        self.assertEqual(data["name"], self.NAME)
        self.assertEqual(data["description"], self.DESCRIPTION)

    def test_get_amenity_not_found(self):
        response = self.client.get(f"{self.URL}/2")
        self.assertEqual(response.status_code, 404)

    def test_put_amenity_updates_name_successfully(self):
        updated_name = "Update Amenity"

        response = self.client.put(f"{self.URL}/1", data={"name": updated_name})
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], updated_name)

    def test_put_amenity_updates_description_successfully(self):
        updated_description = "Update Description"

        response = self.client.put(f"{self.URL}/1", data={"description": updated_description})
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["description"], updated_description)

    def test_put_amenity_name_max_length_exceeded(self):
        exceeded_name = "a" * 101
        response = self.client.put(f"{self.URL}/1", data={"name": exceeded_name})
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data)

    def test_put_amenity_description_max_length_exceeded(self):
        exceeded_description = "a" * 201
        response = self.client.put(f"{self.URL}/1", data={"description": exceeded_description})
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("description", data)

    def test_delete_amenity(self):
        response = self.client.delete(f"{self.URL}/1")
        self.assertEqual(response.status_code, 204)
