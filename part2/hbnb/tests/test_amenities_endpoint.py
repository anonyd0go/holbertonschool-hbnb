import unittest
from app import create_app
import uuid

class TestAmenityEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "WiFi"
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)
        self.assertEqual(response.json["name"], "WiFi")

    def test_create_amenity_invalid_data(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": ""
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_amenities(self):
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_amenity_by_id(self):
        # First, create an amenity to get
        create_response = self.client.post('/api/v1/amenities/', json={
            "name": "WiFi"
        })
        self.assertEqual(create_response.status_code, 201)
        amenity_id = create_response.json["id"]

        # Now, get the amenity by ID
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["id"], amenity_id)
        self.assertEqual(response.json["name"], "WiFi")

    def test_get_amenity_by_id_not_found(self):
        response = self.client.get('/api/v1/amenities/nonexistent_id')
        self.assertEqual(response.status_code, 404)

    def test_update_amenity(self):
        # First, create an amenity to update
        create_response = self.client.post('/api/v1/amenities/', json={
            "name": "WiFi"
        })
        self.assertEqual(create_response.status_code, 201)
        amenity_id = create_response.json["id"]

        # Now, update the amenity
        update_response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "name": "Updated WiFi"
        })
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json["message"], "Amenity updated successfully")

    def test_update_amenity_invalid_data(self):
        # First, create an amenity to update
        create_response = self.client.post('/api/v1/amenities/', json={
            "name": "WiFi"
        })
        self.assertEqual(create_response.status_code, 201)
        amenity_id = create_response.json["id"]

        # Now, try to update the amenity with invalid data
        update_response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "name": ""
        })
        self.assertEqual(update_response.status_code, 400)

    def test_update_amenity_not_found(self):
        update_response = self.client.put('/api/v1/amenities/nonexistent_id', json={
            "name": "Updated WiFi"
        })
        self.assertEqual(update_response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
