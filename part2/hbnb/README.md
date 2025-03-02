# Hbnb - Evolution

This project is a simple Airbnb-like clone built using Python and Flask. The application is structured to separate concerns into different modules, making it easier to manage and scale.

## Project Structure

### Directory and File Purpose

- **app/**: Contains the core application code.
  - **api/**: Houses the API endpoints, organized by version (v1/).
    - **v1/**: Contains version 1 of the API endpoints.
      - **users.py**: API endpoints for user-related operations.
      - **places.py**: API endpoints for place-related operations.
      - **reviews.py**: API endpoints for review-related operations.
      - **amenities.py**: API endpoints for amenity-related operations.
  - **models/**: Contains the business logic classes.
    - **user.py**: Defines the User model.
    - **place.py**: Defines the Place model.
    - **review.py**: Defines the Review model.
    - **amenity.py**: Defines the Amenity model.
  - **services/**: Implements the Facade pattern, managing the interaction between layers.
    - **facade.py**: Contains the Facade class to simplify communication between layers.
  - **persistence/**: Implements the in-memory repository, which will later be replaced by a database-backed solution using SQL Alchemy.
    - **repository.py**: Defines the repository classes for data persistence.
- **tests**: Contains unittests for the application.
- **run.py**: Entry point for running the Flask application.
- **config.py**: Configures environment variables and application settings.
- **requirements.txt**: Lists all the Python packages needed for the project.
- **README.md**: Contains a brief overview of the project.

## Business Logic Layer

### Entities and Responsibilities

- **User**: Represents a user with first name, last name, email, and admin status.
- **Place**: Represents a place with various attributes and related reviews and amenities.
- **Review**: Represents a review with text, rating, place, and user.
- **Amenity**: Represents an amenity with a name.

### Examples

#### Creating a User
```python
from app.models.user import User

# Create a new user
user = User(first_name="John", last_name="Doe", email="john.doe@example.com")

# Access user attributes
print(user.first_name)  # Output: John
print(user.last_name)   # Output: Doe
print(user.email)       # Output: john.doe@example.com
```

#### Creating a Place
```python
from app.models.place import Place

# Create a new place
place = Place(
    title="Cozy Cottage",
    description="A cozy cottage in the countryside.",
    price=100.0,
    latitude=34.0522,
    longitude=-118.2437,
    owner="John Doe"
)

# Access place attributes
print(place.title)       # Output: Cozy Cottage
print(place.description) # Output: A cozy cottage in the countryside.
print(place.price)       # Output: 100.0
```

#### Creating a Review
```python
from app.models.review import Review
from app.models.place import Place
from app.models.user import User

# Create a new user and place
user = User(first_name="John", last_name="Doe", email="john.doe@example.com")
place = Place(
    title="Cozy Cottage",
    description="A cozy cottage in the countryside.",
    price=100.0,
    latitude=34.0522,
    longitude=-118.2437,
    owner="John Doe"
)

# Create a new review
review = Review(
    text="Great place to stay!",
    rating=5,
    place=place,
    user=user
)

# Access review attributes
print(review.text)   # Output: Great place to stay!
print(review.rating) # Output: 5
```

#### Creating an Amenity
```python
from app.models.amenity import Amenity

# Create a new amenity
amenity = Amenity(name="WiFi")

# Access amenity attributes
print(amenity.name)  # Output: WiFi
```


## Installation and Running the Application
### Prerequisites
- Python 3.6+
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```
   sh
   git clone <repository-url>
   cd hbnb
   ```

2. Create virtual environment:
    ```
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

### Runing the Application
1. Set the environment variables (optional):
    ```
    export FLASK_ENV=development
    export SECRET_KEY='your_secret_key'
    ```
    * **vulnerability**: hardcoded-credentials Embedding credentials in source code risks unauthorized access

2. Run the Flask application:
```python run.py```

3. The application will be available in a local server.

### Running Unit Tests
To run the unit tests, you need to update the PYTHONPATH to include the project directory. You can do this from the command line:
```
export PYTHONPATH=$(pwd)
```
Then, you can run the tests using a test runner like `pytest`
