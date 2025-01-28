document.getElementById('postForm').addEventListener('submit', function(event) {
    let isValid = true;
    const content = document.querySelector('textarea[name="content"]');

    // Clear previous error messages
    document.querySelectorAll('.error-message').forEach(el => el.remove());
    document.querySelectorAll('.invalid-field').forEach(el => el.classList.remove('invalid-field'));

    if (content.value.length > 1500) {
        const errorMessage = document.createElement('div');
        errorMessage.className = 'error-message';
        errorMessage.textContent = 'Post content must be at most 1500 characters long.';
        content.classList.add('invalid-field');
        content.parentNode.appendChild(errorMessage);
        isValid = false;
    }

    if (!isValid) {
        event.preventDefault();
    }
});
