import unittest
from app import create_app
import uuid

class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_place(self):
        # First, create a user to associate with the place
        unique_email = f"owner.{uuid.uuid4()}@example.com"
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "User",
            "email": unique_email
        })
        self.assertEqual(user_response.status_code, 201)
        user_id = user_response.json["id"]

        # Now, create a place
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Cottage",
            "description": "A cozy cottage in the countryside.",
            "price": 100.0,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner_id": user_id
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)
        self.assertEqual(response.json["title"], "Cozy Cottage")
        self.assertEqual(response.json["description"], "A cozy cottage in the countryside.")
        self.assertEqual(response.json["price"], 100.0)
        self.assertEqual(response.json["latitude"], 34.0522)
        self.assertEqual(response.json["longitude"], -118.2437)
        self.assertEqual(response.json["owner_id"], user_id)

    def test_create_place_invalid_data(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "description": "",
            "price": -100.0,
            "latitude": 200.0,
            "longitude": 200.0,
            "owner_id": "invalid_id"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_places(self):
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_place_by_id(self):
        # First, create a user to associate with the place
        unique_email = f"owner.{uuid.uuid4()}@example.com"
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "User",
            "email": unique_email
        })
        self.assertEqual(user_response.status_code, 201)
        user_id = user_response.json["id"]

        # Now, create a place
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Cottage",
            "description": "A cozy cottage in the countryside.",
            "price": 100.0,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner_id": user_id
        })
        self.assertEqual(place_response.status_code, 201)
        place_id = place_response.json["id"]

        # Now, get the place by ID
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["id"], place_id)
        self.assertEqual(response.json["title"], "Cozy Cottage")
        self.assertEqual(response.json["description"], "A cozy cottage in the countryside.")
        self.assertEqual(response.json["latitude"], 34.0522)
        self.assertEqual(response.json["longitude"], -118.2437)
        self.assertEqual(response.json["owner"]["id"], user_id)

    def test_get_place_by_id_not_found(self):
        response = self.client.get('/api/v1/places/nonexistent_id')
        self.assertEqual(response.status_code, 404)

    def test_update_place(self):
        # First, create a user to associate with the place
        unique_email = f"owner.{uuid.uuid4()}@example.com"
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "User",
            "email": unique_email
        })
        self.assertEqual(user_response.status_code, 201)
        user_id = user_response.json["id"]

        # Now, create a place
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Cottage",
            "description": "A cozy cottage in the countryside.",
            "price": 100.0,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner_id": user_id
        })
        self.assertEqual(place_response.status_code, 201)
        place_id = place_response.json["id"]

        # Now, update the place
        update_response = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "Updated Cottage",
            "description": "An updated cozy cottage in the countryside.",
            "price": 150.0,
            "latitude": 35.0522,
            "longitude": -119.2437,
            "owner_id": user_id
        })
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json["message"], "Place updated successfully")

    def test_update_place_invalid_data(self):
        # First, create a user to associate with the place
        unique_email = f"owner.{uuid.uuid4()}@example.com"
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "User",
            "email": unique_email
        })
        self.assertEqual(user_response.status_code, 201)
        user_id = user_response.json["id"]

        # Now, create a place
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Cottage",
            "description": "A cozy cottage in the countryside.",
            "price": 100.0,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner_id": user_id
        })
        self.assertEqual(place_response.status_code, 201)
        place_id = place_response.json["id"]

        # Now, try to update the place with invalid data
        update_response = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "",
            "description": "",
            "price": -150.0,
            "latitude": 200.0,
            "longitude": 200.0,
            "owner_id": "invalid_id"
        })
        self.assertEqual(update_response.status_code, 400)

    def test_update_place_not_found(self):
        update_response = self.client.put('/api/v1/places/nonexistent_id', json={
            "title": "Updated Cottage",
            "description": "An updated cozy cottage in the countryside.",
            "price": 150.0,
            "latitude": 35.0522,
            "longitude": -119.2437,
            "owner_id": "nonexistent_id"
        })
        self.assertEqual(update_response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
