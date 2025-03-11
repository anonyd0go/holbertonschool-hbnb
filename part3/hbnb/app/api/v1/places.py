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

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=False, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's"),
    'reviews': fields.List(fields.String, description='List of reviews IDs')
})

""" Defines place model for complex data storing with nested models
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})
"""

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
        a JSON payload with the place's details.

        Returns:
            dict: A dictionary containing the newly created place's details.
            int: The HTTP status code.
        """
        current_user = get_jwt_identity()

        place_data = api.payload
        place_data["owner_id"] = current_user
        if not facade.get_user(place_data["owner_id"]):
            return {"error": "Invalid input data"}, 400

        try:
            new_place = facade.create_place(place_data)
        except Exception:
            return {"error": "Invalid input data"}, 400
        facade.update_user(current_user, {"places": new_place.id})

        return {
            "id": new_place.id,
            "title": new_place.title,
            "description": new_place.description,
            "price": new_place.price,
            "latitude": new_place.latitude,
            "longitude": new_place.longitude,
            "owner_id": current_user
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
        places_list = []
        for place in place_repo_list:
            places_list.append(
                {
                    "id": place.id,
                    "title": place.title,
                    "latitude": place.latitude,
                    "longitude": place.longitude
                }
            )
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
        # TODO: understand how to use fields.Nested for marshaling
        owner = facade.get_user(place.owner_id)
        amenities = [facade.get_amenity(amenity) for amenity in place.amenities]
        reviews = [facade.get_review(review) for review in place.reviews]
        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": marshal(owner, user_model),
            "amenities": [marshal(amenity, amenity_model) for amenity in amenities],
            "reviews": [marshal(review, review_model) for review in reviews]
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

        This endpoint updates a place's details by its ID. It expects
        a JSON payload with the updated place details.

        Args:
            place_id (str): The ID of the place to update.

        Returns:
            dict: A dictionary containing a success message.
            int: The HTTP status code.
        """
        update_place_data = api.payload
        # TODO validate update info user existance, review existance, and amenity existance
        current_user = get_jwt_identity()
        place_to_update = facade.get_place(place_id)

        if not place_to_update:
            return {"error": "Place not found"}, 404
        if place_to_update.owner_id != current_user:
            return {'error': 'Unauthorized action'}, 403
        if not set(update_place_data.keys()).issubset(set(dir(place_to_update))):
            return {"error": "Invalid input data"}, 400

        try:
            facade.update_place(place_id, update_place_data)
        except:
            return {"error": "Invalid input data"}, 400

        return {"message": "Place updated successfully"}, 200


# Did not understand how to get this uri to work from reviews.py
@api.route('/places/<place_id>/reviews', endpoint='places')
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
            facade.get_review(review_id) for review_id in place.reviews
        ]
        reviews_list = [
            {
                "id": review.id,
                "text": review.text,
                "rating": review.rating
            } for review in place_review_list
        ]

        return reviews_list, 200
