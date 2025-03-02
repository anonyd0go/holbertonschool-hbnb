import unittest
from app import create_app
import uuid

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        unique_email = f"jane.doe.{uuid.uuid4()}@example.com"
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": unique_email
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)
        self.assertEqual(response.json["first_name"], "Jane")
        self.assertEqual(response.json["last_name"], "Doe")
        self.assertEqual(response.json["email"], unique_email)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_users(self):
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_user_by_id(self):
        # First, create a user to get
        unique_email = f"john.doe.{uuid.uuid4()}@example.com"
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": unique_email
        })
        self.assertEqual(create_response.status_code, 201)
        self.assertIn("id", create_response.json)
        user_id = create_response.json["id"]

        # Now, get the user by ID
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["id"], user_id)
        self.assertEqual(response.json["first_name"], "John")
        self.assertEqual(response.json["last_name"], "Doe")
        self.assertEqual(response.json["email"], unique_email)

    def test_get_user_by_id_not_found(self):
        response = self.client.get('/api/v1/users/nonexistent_id')
        self.assertEqual(response.status_code, 404)

    def test_update_user(self):
        # First, create a user to update
        unique_email = f"john.doe.{uuid.uuid4()}@example.com"
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": unique_email
        })
        self.assertEqual(create_response.status_code, 201)
        self.assertIn("id", create_response.json)
        user_id = create_response.json["id"]

        # Now, update the user
        unique_email_update = f"johnny.doe.{uuid.uuid4()}@example.com"
        update_response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Johnny",
            "last_name": "Doe",
            "email": unique_email_update
        })
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json["first_name"], "Johnny")
        self.assertEqual(update_response.json["email"], unique_email_update)

    def test_update_user_invalid_data(self):
        # First, create a user to update
        unique_email = f"john.doe.{uuid.uuid4()}@example.com"
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": unique_email
        })
        self.assertEqual(create_response.status_code, 201)
        self.assertIn("id", create_response.json)
        user_id = create_response.json["id"]

        # Now, try to update the user with invalid data
        update_response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(update_response.status_code, 400)

    def test_update_user_not_found(self):
        unique_email_update = f"johnny.doe.{uuid.uuid4()}@example.com"
        update_response = self.client.put('/api/v1/users/nonexistent_id', json={
            "first_name": "Johnny",
            "last_name": "Doe",
            "email": unique_email_update
        })
        self.assertEqual(update_response.status_code, 404)

if __name__ == '__main__':
    unittest.main()