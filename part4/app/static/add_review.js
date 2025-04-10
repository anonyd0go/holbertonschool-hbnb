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
    if (!token) {
        console.warn('User is not authenticated'); // Debugging
        return null; // Return null if the user is not authenticated
    }
    return token;
}

// Function to extract the place ID from the URL
function getPlaceIdFromURL() {
    const pathParts = window.location.pathname.split('/');
    return pathParts[pathParts.length - 1];
}

// Function to submit the review
async function submitReview(token, placeId, reviewText, rating) {
    try {
        const response = await fetch(`/api/v1/reviews/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ text: reviewText, rating: parseInt(rating), place_id: placeId})
        });

        if (response.ok) {
            document.getElementById('success-message').style.display = 'block';
            document.getElementById('error-message').style.display = 'none';
            document.getElementById('review-form').reset(); // Clear the form
            // window.location.href = window.location.pathname;
        } else {
            document.getElementById('success-message').style.display = 'none';
            document.getElementById('error-message').style.display = 'block';
        }
    } catch (error) {
        console.error('Error submitting review:', error);
        document.getElementById('success-message').style.display = 'none';
        document.getElementById('error-message').style.display = 'block';
    }
}

// Event listener for the review form
document.addEventListener('DOMContentLoaded', () => {
    const token = checkAuthentication(); // Check if the user is authenticated
    const placeId = getPlaceIdFromURL(); // Get the place ID from the URL
    const reviewForm = document.getElementById('review-form');

    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault(); // Prevent default form submission behavior

            if (!token) {
                // Redirect to login page if the user is not authenticated
                window.location.href = '/login';
                return;
            }

            const reviewText = document.getElementById('review').value;
            const rating = document.getElementById('rating').value;

            await submitReview(token, placeId, reviewText, rating); // Submit the review
        });
    }
});
