from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Register a new amenity.

        This endpoint allows for the registration of a new amenity. It expects
        a JSON payload with the amenity's name.

        Returns:
            dict: A dictionary containing the newly created amenity's details.
            int: The HTTP status code.
        """
        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
        except Exception:
            return {"error": "Invalid input data"}, 400

        return {
            "id": new_amenity.id,
            "name": new_amenity.name
        }, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """
        Retrieve a list of all amenities.

        Returns:
            list: A list of dictionaries containing amenity details.
            int: The HTTP status code.
        """
        amenity_repo_list = facade.get_all_amenities()
        amenities_list = []
        for amenity in amenity_repo_list:
            amenities_list.append(
                {
                    "id": amenity.id,
                    "name": amenity.name
                }
            )

        return amenities_list, 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """
        Get amenity details by ID.

        Args:
            amenity_id (str): The ID of the amenity to retrieve.

        Returns:
            dict: A dictionary containing the amenity's details.
            int: The HTTP status code.
        """
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error' : 'Amenity not found'}, 404

        return {
            "id": amenity.id,
            "name": amenity.name
        }, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """
        Update an amenity's information.

        This endpoint updates an amenity's details by its ID. It expects
        a JSON payload with the updated amenity details.

        Args:
            amenity_id (str): The ID of the amenity to update.

        Returns:
            dict: A dictionary containing a success message.
            int: The HTTP status code.
        """
        update_amenity_data = api.payload
        amenity_to_update = facade.get_amenity(amenity_id)
        if not amenity_to_update:
            return {'error': 'Amenity not found'}, 404
        try:
            facade.update_amenity(amenity_id, update_amenity_data)
        except Exception:
            return {"error": "Invalid input data"}, 400

        return {"message" : "Amenity updated successfully"}, 200
