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
- **run.py**: Entry point for running the Flask application.
- **config.py**: Configures environment variables and application settings.
- **requirements.txt**: Lists all the Python packages needed for the project.
- **README.md**: Contains a brief overview of the project.

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
