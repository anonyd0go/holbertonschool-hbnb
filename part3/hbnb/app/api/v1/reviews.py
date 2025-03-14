from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    # 'user_id': fields.String(required=True, description='ID of the user'),
    # 'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """
        Register a new review.

        This endpoint allows an authenticated user to create a new review.
        The user_id is taken from the JWT token and cannot be overridden.

        Returns:
            dict: A dictionary containing the newly created review's details.
            int: The HTTP status code.
        """
        current_user = get_jwt_identity()
        review_data = api.payload

        review_data["user_id"] = current_user

        place_to_review = facade.get_place(review_data["place_id"])
        if not place_to_review:
            return {"error": "Place not found"}, 400

        user_giving_review = facade.get_user(current_user)
        if not user_giving_review:
            return {"error": "User not found"}, 400
        if review_data["place_id"] in [plc.id for plc in facade.get_places_by_owner(current_user)]:
            return {"error": "You cannot review your own place"}, 400

        for review_id in place_to_review.reviews:
            review = facade.get_review(review_id)
            if review and review.user_id == current_user:
                return {"error": "You have already reviewed this place"}, 400

        try:
            new_review = facade.create_review(review_data)
        except Exception as e:
            return {"error": f"Invalid input data {str(e)}"}, 400

        return {
            "id": new_review.id,
            "text": new_review.text,
            "rating": new_review.rating,
            "user_id": new_review.user_id,
            "place_id": new_review.place_id
        }, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """
        Retrieve a list of all reviews.

        Returns:
            list: A list of dictionaries containing review details.
            int: The HTTP status code.
        """
        review_repo_list = facade.get_all_reviews()
        reviews_list = [
            {
                "id": review.id,
                "text": review.text,
                "rating": review.rating
            } for review in review_repo_list
        ]

        return reviews_list, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """
        Get review details by ID.

        Args:
            review_id (str): The ID of the review to retrieve.

        Returns:
            dict: A dictionary containing the review's details.
            int: The HTTP status code.
        """
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        return {
            "id": review.id,
            "text": review.text,
            "rating": review.rating,
            "user_id": review.user_id,
            "place_id": review.place_id
        }, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, review_id):
        """
        Update a review's details.

        This endpoint updates a review. Only the author of the review can update it,
        and only fields allowed by the review_model (text and rating) can be modified.

        Args:
            review_id (str): The ID of the review to update.

        Returns:
            dict: A dictionary containing a success message.
            int: The HTTP status code.
        """
        current_user = get_jwt_identity()

        update_review_data = api.payload
        review_to_update = facade.get_review(review_id)
        allowed_update = {"text", "rating"}

        if not review_to_update:
            return {"error": "Review not found"}, 404
        if review_to_update.user_id != current_user:
            return {"error": "Unauthorized action"}, 403
        if not set(update_review_data.keys()).issubset(allowed_update):
            return {"error": "Invalid input data: Only text and rating can be updated"}, 400

        try:
            facade.update_review(review_id, update_review_data)
        except Exception as e:
            return {"error": f"Invalid input data {str(e)}"}, 400

        return {"message": "Review updated successfully"}, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def delete(self, review_id):
        """
        Delete a review by its ID.

        Args:
            review_id (str): The ID of the review to delete.

        Returns:
            dict: A dictionary containing a success message.
            int: The HTTP status code.
        """
        current_user = get_jwt_identity()

        review_to_delete = facade.get_review(review_id)
        if not review_to_delete:
            return {"error": "Review not found"}, 404
        if review_to_delete.user_id != current_user:
            return {"error": "Unauthorized action"}, 403

        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200
