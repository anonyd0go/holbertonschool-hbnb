from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})


@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Register a new user.

        This endpoint allows for the registration of a new user. It expects
        a JSON payload with the user's first name, last name, and email.

        Returns:
            dict: A dictionary containing the newly created user's details.
            int: The HTTP status code.
        """
        user_data = api.payload

        # Simulate email uniqueness check (to be replaced by real validation with persistence)
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
        except Exception:
            return {"error": "Invalid input data"}, 400

        return {
            'id': new_user.id,
            'message': "User successfully crated"
            }, 201

    @api.response(200, "All users succesfully retrieved")
    def get(self):
        """
        Retrieve all users.

        This endpoint retrieves all users from the repository.

        Returns:
            list: A list of dictionaries containing user details.
            int: The HTTP status code.
        """
        user_repo_list = facade.get_users_all()
        user_list = []
        for user in user_repo_list:
            user_list.append(
                {
                    'id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email
                }
            )

        return user_list, 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Get user details by ID.

        This endpoint retrieves a user's details by their ID.

        Args:
            user_id (str): The ID of the user to retrieve.

        Returns:
            dict: A dictionary containing the user's details.
            int: The HTTP status code.
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'places': user.places
        }, 200

    @api.expect(user_model)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """
        Update user details by ID.

        This endpoint updates a user's details by their ID. It expects
        a JSON payload with the updated user details.

        Args:
            user_id (str): The ID of the user to update.

        Returns:
            dict: A dictionary containing the updated user's details.
            int: The HTTP status code.
        """
        update_user_data = api.payload
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
        if not set(update_user_data.keys()).issubset(set(dir(user))):
            return {"error": "Invalid input data"}, 400

        # TODO validate places exist if it will be modified or find how to remove it if desired
        try:
            facade.update_user(user_id, update_user_data)
        except Exception:
            return {"error": "Invalid input data"}, 400
        updated_user = facade.get_user(user_id)

        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email,
            'places': updated_user.places
        }, 200
