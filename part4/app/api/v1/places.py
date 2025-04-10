from flask_restx import Namespace, Resource, fields, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

# Defines place model for complex data storing with nested models
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    #'owner_id': fields.String(required=True, description='ID of the owner'),
    #'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def post(self):
        """
        Register a new place.

        This endpoint allows for the registration of a new place. It expects
        a JSON payload with the place's details. The owner is determined from
        the JWT token.

        Returns:
            dict: A dictionary containing the newly created place's details.
            int: The HTTP status code.
        """
        current_user = get_jwt_identity()

        place_data = api.payload

        place_data["owner_id"] = current_user
        if not facade.get_user(current_user):
            return {"error": "Invalid input data"}, 400

        try:
            new_place = facade.create_place(place_data)
        except Exception as e:
            return {"error": f"Invalid input data {str(e)}"}, 400

        return {
            "id": new_place.id,
            "title": new_place.title,
            "description": new_place.description,
            "price": new_place.price,
            "latitude": new_place.latitude,
            "longitude": new_place.longitude,
            "owner": marshal(facade.get_user(new_place.owner_id), user_model)
        }, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """
        Retrieve a list of all places from the repository.

        Returns:
            list: A list of dictionaries containing place details.
            int: The HTTP status code.
        """
        place_repo_list = facade.get_all_places()
        places_list = [{
            "id": place.id,
            "title": place.title,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "price": place.price
        } for place in place_repo_list]
        return places_list, 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Get place details by ID.

        Args:
            place_id (str): The ID of the place to retrieve.

        Returns:
            dict: A dictionary containing the place's details.
            int: The HTTP status code.
        """
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        owner = facade.get_user(place.owner_id)
        amenities = [facade.get_amenity(amenity.id) for amenity in place.amenities]
        reviews = [facade.get_review(review.id) for review in place.reviews]
        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "price": place.price,
            "rating": facade.get_average_rating_for_place(place.id),
            "owner": marshal(owner, user_model) if owner else None,
            "amenities": [marshal(amenity, amenity_model) for amenity in amenities if amenity],
            "reviews": [marshal(review, review_model) for review in reviews if review]
        }, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, place_id):
        """
        Update a place's information.

        This endpoint updates a place's details by its ID. Only the owner
        can update the place.

        Args:
            place_id (str): The ID of the place to update.

        Returns:
            dict: A dictionary containing a success message.
            int: The HTTP status code.
        """
        current_user = get_jwt_identity()
        update_place_data = api.payload

        place_to_update = facade.get_place(place_id)
        allowed_update = {
            "title", "description",
            "price", "latitude", "longitude"
        }

        if not place_to_update:
            return {"error": "Place not found"}, 404
        if place_to_update.owner_id != current_user:
            return {'error': 'Unauthorized action'}, 403
        if not set(update_place_data.keys()).issubset(allowed_update):
            return {"error": "Invalid input data"}, 400

        try:
            facade.update_place(place_id, update_place_data)
        except Exception as e:
            return {"error": f"Invalid input data {str(e)}"}, 400

        return {"message": "Place updated successfully"}, 200


@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Get all reviews for a specific place.

        This endpoint retrieves all reviews for a specific place by its ID.

        Args:
            place_id (str): The ID of the place to retrieve reviews for.

        Returns:
            list: A list of dictionaries containing review details.
            int: The HTTP status code.
        """
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        place_review_list = [
            marshal(facade.get_review(review.id), review_model) for review in place.reviews if review
        ]
        return place_review_list, 200
