from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource


api = Namespace('protected', description='Protected route')

@api.route('/', strict_slashes=False)
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """
        A protected endpoint that requires a valid JWT token.

        This endpoint can only be accessed by users with a valid JWT token.
        It retrieves the user's identity from the token and returns a greeting message.

        Returns:
            dict: A dictionary containing a greeting message.
            int: The HTTP status code.
        """
        current_user = get_jwt_identity()  # Retrieve the user's identity from the token
        return {
            'message': f'Hello, user {current_user}',
            }, 200
