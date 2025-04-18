from flask import Blueprint, render_template, session, redirect, url_for

html = Blueprint('html', __name__)


@html.route('/')
def root_redirect():
    """
    Redirect the root URL to /home.

    Returns:
        Redirect: Redirect to /home.
    """
    return redirect(url_for('html.index'))

@html.route('/home')
def index():
    """
    Render the home page.

    Returns:
        HTML: The home page.
    """
    return render_template('index.html')

@html.route('/login')
def login():
    """
    Render the login page.

    Returns:
        HTML: The login page.
    """
    return render_template('login.html')

@html.route('/logout')
def logout():
    """
    Log out the user and redirect to the login page.

    Returns:
        HTML: The login page.
    """
    session.pop('user', None)
    session.pop('access_token', None)
    session.clear()
    return redirect(url_for('html.login'))

@html.route('/place/<place_id>')
def place_details(place_id):
    """
    Render the place details page.

    Args:
        place_id (str): The ID of the place to display.

    Returns:
        HTML: The place details page.
    """
    return render_template('place.html', place_id=place_id)
