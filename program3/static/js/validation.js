function validateForm() {
    // Basic validation for email and phone number
    var email = document.getElementById("email").value;
    var phone = document.getElementById("phone").value;

    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    var phoneRegex = /^\d{10}$/;

    if (!emailRegex.test(email)) {
        alert("Please enter a valid email address.");
        return false;
    }

    if (!phoneRegex.test(phone)) {
        alert("Please enter a valid phone number (10 digits only).");
        return false;
    }

    // You can add more validation rules as needed

    return true;
}



document.getElementById("registrationForm").onsubmit = function () {
    if (validateForm()) {
        // Redirect to the login page after successful registration
        window.location.href = "/login";
    }
    return false; // Prevent the form from submitting normally
};
