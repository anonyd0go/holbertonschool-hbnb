from flask_restx import Namespace, Resource, fields, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade


api = Namespace('admin', description='Admin operations')


#-----Marshaling models-----#
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

user_model = api.model('User', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'password': fields.String(description='Password of the user'),
    'is_admin': fields.Boolean(description='Admin status of the user')
})

#-----Admin Endpoint logic-----#
@api.route('/users/<user_id>')
class AdminUserResource(Resource):
    @api.expect(user_model)
    @api.response(400, 'Invalid input data')
    @api.response(400, 'Email is already in use')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'User not found')
    @api.response(200, 'User succesfully updated')
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()
        user_jwt = get_jwt()

        # If 'is_admin' is part of the identity payload
        if current_user and not user_jwt["is_admin"]:
            return {'error': 'Admin privileges required'}, 403

        user_to_update = facade.get_user(user_id)
        if not user_to_update:
            return {'error': 'User not found'}, 404

        user_update_data = api.payload
        if not set(user_update_data.keys()).issubset(set(user_model)):
            return {'error': 'Invalid input data'}, 400

        if user_update_data["email"]:
            # Check if email is already in use
            existing_user = facade.get_user_by_email(user_update_data["email"])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email is already in use'}, 400

        try:
            facade.update_user(user_id, user_update_data)
        except Exception:
            return {"error": "Invalid input data"}, 400
        updated_user = facade.get_user(user_id)

        return {
            "message": "User updated successfully",
            "user": marshal(updated_user, user_model),
            "user_places":updated_user.places,
            "user_reviews": updated_user.reviews
        }, 200


@api.route('/users/')
class AdminUserCreate(Resource):
    @api.expect(user_model)
    @api.response(201, 'User succesfully created')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        user_jwt = get_jwt()

        if current_user and not user_jwt["is_admin"]:
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload
        if not set(user_data.keys()).issubset(set(user_model)):
            return {'error': 'Invalid input data'}, 400

        # Check if email is already in use
        if facade.get_user_by_email(user_data["email"]):
            return {'error': 'Email already registered'}, 400

        # Logic to create a new user
        try:
            new_user = facade.create_user(user_data)
        except Exception as e:
            return {"error": f"Invalid input data {e}"}, 400
        
        return {
            'id': new_user.id,
            'message': "User successfully crated"
        }, 201


@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        user_jwt = get_jwt()

        if current_user and not user_jwt["is_admin"]:
            return {'error': 'Admin privileges required'}, 403

        # Logic to create a new amenity
        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
        except Exception as e:
            return {"error": f"Invalid input data {str(e)}"}, 400
        
        return {
            "id": new_amenity.id,
            "name": new_amenity.name
        }, 201


@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'Amenity not found')
    @jwt_required()
    def put(self, amenity_id):
        current_user = get_jwt_identity()
        user_jwt = get_jwt()

        if current_user and not user_jwt["is_admin"]:
            return {'error': 'Admin privileges required'}, 403
        
        update_amenity_data = api.payload
        amenity_to_update = facade.get_amenity(amenity_id)
        if not amenity_to_update:
            return {'error': 'Amenity not found'}, 404

        try:
            facade.update_amenity(amenity_id, update_amenity_data)
        except Exception as e:
            return {"error": f"Invalid input data {str(e)}"}, 400

        return {"message" : "Amenity updated successfully"}, 200


@api.route('/places/<place_id>')
class AdminPlaceModify(Resource):
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized action')
    @jwt_required()
    def put(self, place_id):
        current_user = get_jwt_identity()
        user_jwt = get_jwt()

        place_to_update = facade.get_place(place_id)
        if not place_to_update:
            return {"error": "Place not found"}, 404
        if not user_jwt["is_admin"] and place_to_update.owner_id != current_user:
            return {'error': 'Unauthorized action'}, 403

        # Logic to update the place
        update_place_data = api.payload
        try:
            facade.update_place(place_id, update_place_data)
        except Exception as e:
            return {"error": f"Invalid input data {str(e)}"}, 400

        return {"message": "Place updated successfully"}, 200
