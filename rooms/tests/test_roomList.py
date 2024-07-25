from rest_framework.test import APITestCase
from rooms.models import Room, Amenity
from users.models import User
from categories.models import Category


class TestRoomList(APITestCase):

    URL = "/api/v1/rooms/"

    name = "Create Room Test - name"
    price = 1
    number_of_rooms = 1
    bathrooms = 1
    description = "Create Room Test - description"
    address = "Create Room Test - address"
    room_type = Room.TypeChoices.ENTIRE_PLACE

    def setUp(self):
        self.user = User.objects.create(username="test")
        self.category = Category.objects.create(name="Test Category", kind=Category.CategoryKindChoices.ROOMS)
        self.amenity = Amenity.objects.create(name="Test Amenity")

    def test_create_room_without_authentication(self):

        response = self.client.post(self.URL)
        self.assertEqual(response.status_code, 403)

    # Test for meeting required field - name
    def test_create_room_with_missing_fields(self):

        self.client.force_login(self.user)

        print(self.amenity.id)

        response = self.client.post(
            self.URL,
            data={
                "name": self.name,
                "price": self.price,
                "number_of_rooms": self.number_of_rooms,
                "bathrooms": self.bathrooms,
                "description": self.description,
                "address": self.address,
                "room_type": self.room_type,
                "category": self.category.id,
                # "amenities": [self.amenity.id],
            },
            format="json",
        )
        data = response.json()
        print(response, data)
        # expected_errors = {
        #     "name": ["This field is required."],
        #     "price": ["This field is required."],
        #     "number_of_rooms": ["This field is required."],
        #     "bathrooms": ["This field is required."],
        #     "description": ["This field is required."],
        #     "address": ["This field is required."],
        #     "room_type": ["This field is required."],
        # }

        self.assertEqual(response.status_code, 400)
        # self.assertDictEqual(data, expected_errors)

    def test_create_room_success(self):

        self.client.force_login(self.user)

        response = self.client.post(
            self.URL,
            data={
                "name": self.name,
                "price": self.price,
                "number_of_rooms": self.number_of_rooms,
                "bathrooms": self.bathrooms,
                "description": self.description,
                "address": self.address,
                "room_type": self.room_type,
                "category": self.category.id,
                "amenities": [self.amenity.id],
            },
            format="json",
        )
        data = response.json()
        print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], self.name)
        self.assertEqual(data["price"], self.price)
        self.assertEqual(data["number_of_rooms"], self.number_of_rooms)
        self.assertEqual(data["bathrooms"], self.bathrooms)
        self.assertEqual(data["description"], self.description)
        self.assertEqual(data["address"], self.address)
        self.assertEqual(data["room_type"], self.room_type)
        self.assertEqual(data["category"], self.category.id)
        self.assertIn(self.amenity.id, [amenity["id"] for amenity in data["amenities"]])
