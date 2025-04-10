# Part 4: Simple Web Client

This phase focuses on the front-end development of the HBnB application, integrating it with the back-end services developed in previous parts. The goal is to design and implement an interactive user interface using **HTML5**, **CSS3**, and **JavaScript ES6** while leveraging RESTful APIs for dynamic data interaction.

## Features

### Front-End
- **Dynamic Place Listings**:
  - Places are fetched dynamically from the back-end API and displayed on the homepage.
  - Users can filter places by price using a dropdown menu.

- **Place Details Page**:
  - Displays detailed information about a selected place, including its title, description, price, and amenities.
  - Includes a section for user reviews with dynamic population.

- **User Authentication**:
  - Login functionality using JWT tokens.
  - Authenticated users can add reviews for places.

- **Responsive Design**:
  - The interface is styled with CSS3 to ensure a clean and responsive user experience.

### Back-End Integration
- **RESTful API Endpoints**:
  - Endpoints for places, reviews, and authentication are consumed by the front-end.
  - Secure API calls using JWT for authenticated operations.

- **CRUD Operations**:
  - Users can create, read, update, and delete reviews.
  - Admins can manage places and amenities.

### Database
- **MySQL Database**:
  - Tables for users, places, reviews, and amenities.
  - Relationships between tables ensure data integrity (e.g., foreign keys for user and place IDs in reviews).

### JavaScript Functionality
- **Dynamic Content Loading**:
  - JavaScript functions fetch and display data dynamically without requiring page reloads.
  - Example: `fetchPlaces()` retrieves and displays places on the homepage.

- **Client-Side Filtering**:
  - Users can filter places by price range using the `setupPriceFilter()` function.

- **Review Submission**:
  - Authenticated users can submit reviews for places via a form.
  - Reviews are validated and sent to the back-end API.


## How to Run

1. **Set Up the Database**:
   - Use the provided `hbnb_database.sql` file to create and populate the database.
   - Uncomment the `CREATE DATABASE` and `USE` statements if needed.

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
  ```bash
  python run.py
  ```

4 **Access the Application**:
  * Opne your browser and navigate to `http://127.0.0.1:5000/home`

## Future Improvements
* Add more advanced filtering options (e.g., by location or amenities).
* Implement user registration and profile management.
* Enhance the UI with animations and transitions.
