// -------------------- Login -Related Functions --------------------

// Function to log in a user
async function loginUser(email, password) {
    return fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });
}

// Function to logout a user
function logoutUser() {
    // Clear the JWT token cookie
    document.cookie = "token=; path=/; expires=Thu, 01 Jan 1970 00:00:00 UTC;";
    // Redirect to the login page
    window.location.href = '/login';
}

// Function to get a cookie value by its name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Function to check if the user is authenticated
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-button');

    if (!token) {
        if (loginLink) loginLink.style.display = 'inline-block';
    } else {
        if (loginLink) loginLink.style.display = 'none';
    }
}

// -------------------- Index Page Functions --------------------

// Function to populate the price filter dropdown
function populatePriceFilter() {
    const priceFilter = document.getElementById('price-filter');
    if (!priceFilter) {
        return; // Exit the function if the element does not exist
    }

    const priceOptions = [10, 50, 100, 'All'];

    priceOptions.forEach(price => {
        const option = document.createElement('option');
        option.value = price === 'All' ? 'all' : price;
        option.textContent = price === 'All' ? 'All' : `$${price}`;
        priceFilter.appendChild(option);
    });
}

// Function to fetch places data from the API
async function fetchPlaces(token = null) {
    try {
        const headers = {
            'Content-Type': 'application/json'
        };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch('/api/v1/places', {
            method: 'GET',
            headers: headers
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        } else {
            console.error('Failed to fetch places:', response.statusText);
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

// Function to display places dynamically
function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) {
        return; // Exit the function if the element does not exist
    }
    placesList.innerHTML = ''; // Clear the current content

    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';

        placeCard.innerHTML = `
            <h3>${place.title}</h3>
            <p class="place-price">Price: $${place.price}</p>
            <button class="view-details-button" data-id="${place.id}">View Details</button>
        `;

        // Add event listener to the "View Details" button
        const viewDetailsButton = placeCard.querySelector('.view-details-button');
        viewDetailsButton.addEventListener('click', () => {
            window.location.href = `/place/${place.id}`;
        });

        placesList.appendChild(placeCard);
    });
}

// Function to set up client-side filtering
function setupPriceFilter() {
    const priceFilter = document.getElementById('price-filter');
    if (!priceFilter) {
        return; // Exit function if element does not exist
    }

    priceFilter.addEventListener('change', (event) => {
        const selectedPrice = event.target.value;
        const placesList = document.querySelectorAll('.place-card');

        placesList.forEach(placeCard => {
            const priceText = placeCard.querySelector('.place-price').textContent;
            const price = parseFloat(priceText.replace('Price: $', ''));

            if (selectedPrice === 'all' || price <= parseFloat(selectedPrice)) {
                placeCard.style.display = 'block';
            } else {
                placeCard.style.display = 'none';
            }
        });
    });
}

// -------------------- Event Listener for DOMContentLoaded --------------------

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const token = getCookie('token');

    // Handle login form submission
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault(); // Prevent default form submission behavior

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await loginUser(email, password);

                if (response.ok) {
                    const data = await response.json();
                    // Store the JWT token in a cookie
                    document.cookie = `token=${data.access_token}; path=/`;
                    // Fetch places after login
                    fetchPlaces(data.access_token);
                    // Redirect to the main page
                    window.location.href = '/home';
                } else {
                    // Display an error message if login fails
                    alert('Login failed: Invalid email or password');
                }
            } catch (error) {
                console.error('Error during login:', error);
                alert('An error occurred. Please try again later.');
            }
        });
    }

    fetchPlaces(token);

    // Initialize the index page
    populatePriceFilter(); // Populate the price filter options
    setupPriceFilter(); // Set up the price filter functionality
    checkAuthentication(); // Check user authentication and fetch places if authenticated
});
