document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

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
});

async function loginUser(email, password) {
    // Replace '/api/v1/auth/login' with your actual API endpoint
    return fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });
}
/*const token = sessionStorage.getItem('access_token'); // Or retrieve it from cookies/session

fetch('/api/v1/protected-endpoint', {
    method: 'GET',
    headers: {
        'Authorization': `Bearer ${token}`
    }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));*/
/* TODO Implement scripts */ 
