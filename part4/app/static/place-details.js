// Function to extract the place ID from the URL
function getPlaceIdFromURL() {
    const pathParts = window.location.pathname.split('/');
    return pathParts[pathParts.length - 1]; // Get the last part of the path
}

// Function to fetch place details from the API
async function fetchPlaceDetails(placeId) {
    try {
        const response = await fetch(`/api/v1/places/${placeId}`);
        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            console.error('Failed to fetch place details:', response.statusText);
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
    }
}

// Function to display place details dynamically
function displayPlaceDetails(place) {
    const placeDetailsSection = document.getElementById('place-details');
    placeDetailsSection.innerHTML = ''; // Clear the current content

    const placeInfo = document.createElement('div');
    placeInfo.className = 'place-info';

    placeInfo.innerHTML = `
        <h1>${place.title}</h1>
        <p>Host: ${place.owner.first_name} ${place.owner.last_name}</p>
        <p>Price: $${place.price}</p>
        <p>${place.description}</p>
        <h3>Amenities:</h3>
        <ul>
            ${place.amenities.map(amenity => `<li>${amenity.name}</li>`).join('')}
        </ul>
    `;

    placeDetailsSection.appendChild(placeInfo);

    // Populate reviews
    const reviewsSection = document.getElementById('reviews');
    reviewsSection.innerHTML = '<h2>Reviews</h2>';
    if (place.reviews.length > 0) {
        place.reviews.forEach(review => {
            const reviewCard = document.createElement('div');
            reviewCard.className = 'review-card';
            reviewCard.innerHTML = `
                <p>${review.text}</p>
                <p>Rating: ${review.rating} Stars</p>
            `;
            reviewsSection.appendChild(reviewCard);
        });
    } else {
        reviewsSection.innerHTML += '<p>No reviews yet.</p>';
    }
}

// Event Listener for Place Details Page
document.addEventListener('DOMContentLoaded', () => {
    const placeId = getPlaceIdFromURL();
    if (placeId) {
        fetchPlaceDetails(placeId); // Fetch and display place details
    }
});
