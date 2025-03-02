from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Register a new review.

        This endpoint allows for the registration of a new review. It expects
        a JSON payload with the review's details.

        Returns:
            dict: A dictionary containing the newly created review's details.
            int: The HTTP status code.
        """
        review_data = api.payload
        if not facade.get_user(review_data["user_id"]) or not facade.get_place(review_data["place_id"]):
            return {"error": "Invalid input data"}, 400

        try:
            new_review = facade.create_review(review_data)
        except Exception as e:
            return {"error": "Invalid input data {}".format(e)}, 400
        facade.update_place(new_review.place_id, {"reviews": new_review.id})

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
        Retrieve a list of all reviews from the repository.

        Returns:
            list: A list of dictionaries containing review details.
            int: The HTTP status code.
        """
        review_repo_list = facade.review_repo.get_all()
        reviews_list = []
        for review in review_repo_list:
            reviews_list.append(
                {
                    "id": review.id,
                    "text": review.text,
                    "rating": review.rating
                }
            )

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
    def put(self, review_id):
        """
        This endpoint updates a review's details by its ID. It expects
        a JSON payload with the updated review details.

        Args:
            review_id (str): The ID of the review to update.

        Returns:
            dict: A dictionary containing a success message.
            int: The HTTP status code.
        """
        update_review_data = api.payload
        review_to_update = facade.get_review(review_id)
        if not review_to_update:
            return {"error": "Review not found"}, 404
        if not set(update_review_data.keys()).issubset(set(dir(review_to_update))):
            return {"error": "Invalid input data"}, 400

        # TODO: validate user_id and place_id :: Isn't it be better to avoid modifying these?
        try:
            facade.update_review(review_id, update_review_data)
        except:
            return {"error": "Invalid input data"}, 400

        return {"message": "Review updated succesfully"}, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """
        This endpoint deletes a review by its ID.

        Args:
            review_id (str): The ID of the review to delete.

        Returns:
            dict: A dictionary containing a success message.
            int: The HTTP status code.
        """
        review_to_delete = facade.get_review(review_id)
        if not review_to_delete:
            return {"error": "Review not found"}, 404

        # Update place.reviews persistance after review removal
        associated_place = facade.get_place(review_to_delete.place_id)
        associated_place.remove_review(review_id)
        facade.update_place(associated_place.id, {"reviews": associated_place.reviews})

        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200

# Could not get /places/<place_id>/reviews to work from this endpoint
