from flask import render_template
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade

api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """
        Authenticate user and return a JWT token.

        This endpoint allows a user to log in by providing their email and password.
        If the credentials are valid, a JWT token is returned.

        Returns:
            dict: A dictionary containing the JWT token.
            int: The HTTP status code.
        """
        credentials = api.payload  # Get the email and password from the request payload
        
        # Step 1: Retrieve the user based on the provided email
        user = facade.get_user_by_email(credentials['email'])
        
        # Step 2: Check if the user exists and the password is correct
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Step 3: Create a JWT token with the user's id and is_admin flag
        access_token = create_access_token(
            identity=str(user.id), additional_claims={'is_admin': user.is_admin}
        )
        
        # Step 4: Return the JWT token to the client
        return {'access_token': access_token}, 200
    
    def get(self):
        """
        Render the login page.

        This endpoint serves the login.html template when a GET request is made.

        Returns:
            HTML: The login page.
        """
        return render_template('login.html')
