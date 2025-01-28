document.getElementById('profileForm').addEventListener('submit', function(event) {
    var websiteField = document.getElementById('id_website');
    var website = websiteField.value;
    if (website && !website.startsWith('http')) {
        alert('Website URL must start with http or https.');
        event.preventDefault();
    }

    var bioField = document.getElementById('id_bio');
    var bio = bioField.value;
    if (bio.length > 500) {
        alert('Bio must be at most 500 characters long.');
        event.preventDefault();
    }

    var birthDateField = document.getElementById('id_birth_date');
    var birthDate = new Date(birthDateField.value);
    var today = new Date();
    var maxAge = 1115;
    if (birthDate && (today.getFullYear() - birthDate.getFullYear()) > maxAge) {
        alert('Birth date cannot be more than 1115 years ago.');
        event.preventDefault();
    }

    var imageField = document.getElementById('id_image');
    var image = imageField.files[0];
    if (image && image.size > 5 * 1024 * 1024) {  // 5 MB limit
        alert('Image file size must be under 5MB.');
        event.preventDefault();
    }

    var locationField = document.getElementById('id_location');
    var location = locationField.value;
    if (location.length > 255) {
        alert('Location must be at most 255 characters long.');
        event.preventDefault();
    }
});
