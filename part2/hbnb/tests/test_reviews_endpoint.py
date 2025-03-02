import unittest
from app import create_app
import uuid

class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_review(self):
        # First, create a user to associate with the review
        unique_email = f"user.{uuid.uuid4()}@example.com"
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "User",
            "last_name": "Test",
            "email": unique_email
        })
        self.assertEqual(user_response.status_code, 201)
        user_id = user_response.json["id"]

        # Now, create a place to associate with the review
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A place for testing.",
            "price": 100.0,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner_id": user_id
        })
        self.assertEqual(place_response.status_code, 201)
        place_id = place_response.json["id"]

        # Now, create a review
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": user_id,
            "place_id": place_id
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)
        self.assertEqual(response.json["text"], "Great place!")
        self.assertEqual(response.json["rating"], 5)
        self.assertEqual(response.json["user_id"], user_id)
        self.assertEqual(response.json["place_id"], place_id)

    def test_create_review_invalid_data(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 6,
            "user_id": "invalid_id",
            "place_id": "invalid_id"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_reviews(self):
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_review_by_id(self):
        # First, create a user to associate with the review
        unique_email = f"user.{uuid.uuid4()}@example.com"
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "User",
            "last_name": "Test",
            "email": unique_email
        })
        self.assertEqual(user_response.status_code, 201)
        user_id = user_response.json["id"]

        # Now, create a place to associate with the review
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A place for testing.",
            "price": 100.0,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner_id": user_id
        })
        self.assertEqual(place_response.status_code, 201)
        place_id = place_response.json["id"]

        # Now, create a review
        review_response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": user_id,
            "place_id": place_id
        })
        self.assertEqual(review_response.status_code, 201)
        review_id = review_response.json["id"]

        # Now, get the review by ID
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["id"], review_id)
        self.assertEqual(response.json["text"], "Great place!")
        self.assertEqual(response.json["rating"], 5)
        self.assertEqual(response.json["user_id"], user_id)
        self.assertEqual(response.json["place_id"], place_id)

    def test_get_review_by_id_not_found(self):
        response = self.client.get('/api/v1/reviews/nonexistent_id')
        self.assertEqual(response.status_code, 404)

    def test_update_review(self):
        # First, create a user to associate with the review
        unique_email = f"user.{uuid.uuid4()}@example.com"
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "User",
            "last_name": "Test",
            "email": unique_email
        })
        self.assertEqual(user_response.status_code, 201)
        user_id = user_response.json["id"]

        # Now, create a place to associate with the review
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A place for testing.",
            "price": 100.0,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner_id": user_id
        })
        self.assertEqual(place_response.status_code, 201)
        place_id = place_response.json["id"]

        # Now, create a review
        review_response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": user_id,
            "place_id": place_id
        })
        self.assertEqual(review_response.status_code, 201)
        review_id = review_response.json["id"]

        # Now, update the review
        update_response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Updated review",
            "rating": 4
        })
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(update_response.json["message"], "Review updated successfully")

    def test_update_review_invalid_data(self):
        # First, create a user to associate with the review
        unique_email = f"user.{uuid.uuid4()}@example.com"
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "User",
            "last_name": "Test",
            "email": unique_email
        })
        self.assertEqual(user_response.status_code, 201)
        user_id = user_response.json["id"]

        # Now, create a place to associate with the review
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A place for testing.",
            "price": 100.0,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner_id": user_id
        })
        self.assertEqual(place_response.status_code, 201)
        place_id = place_response.json["id"]

        # Now, create a review
        review_response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": user_id,
            "place_id": place_id
        })
        self.assertEqual(review_response.status_code, 201)
        review_id = review_response.json["id"]

        # Now, try to update the review with invalid data
        update_response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "",
            "rating": 6
        })
        self.assertEqual(update_response.status_code, 400)

    def test_update_review_not_found(self):
        update_response = self.client.put('/api/v1/reviews/nonexistent_id', json={
            "text": "Updated review",
            "rating": 4
        })
        self.assertEqual(update_response.status_code, 404)

    def test_delete_review(self):
        # First, create a user to associate with the review
        unique_email = f"user.{uuid.uuid4()}@example.com"
        user_response = self.client.post('/api/v1/users/', json={
            "first_name": "User",
            "last_name": "Test",
            "email": unique_email
        })
        self.assertEqual(user_response.status_code, 201)
        user_id = user_response.json["id"]

        # Now, create a place to associate with the review
        place_response = self.client.post('/api/v1/places/', json={
            "title": "Test Place",
            "description": "A place for testing.",
            "price": 100.0,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "owner_id": user_id
        })
        self.assertEqual(place_response.status_code, 201)
        place_id = place_response.json["id"]

        # Now, create a review
        review_response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": user_id,
            "place_id": place_id
        })
        self.assertEqual(review_response.status_code, 201)
        review_id = review_response.json["id"]

        # Now, delete the review
        delete_response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(delete_response.json["message"], "Review deleted successfully")

    def test_delete_review_not_found(self):
        delete_response = self.client.delete('/api/v1/reviews/nonexistent_id')
        self.assertEqual(delete_response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
