document.getElementById('reviewForm').addEventListener('submit', function(event) {
    let isValid = true;
    const title = document.querySelector('input[name="title"]');
    const content = document.querySelector('textarea[name="content"]');
    const gamerate = document.querySelector('select[name="gamerate"]');

    // Clear previous error messages
    document.querySelectorAll('.error-message').forEach(el => el.remove());
    document.querySelectorAll('.invalid-field').forEach(el => el.classList.remove('invalid-field'));

    if (title.value.length < 5 || title.value.length > 255) {
        const errorMessage = document.createElement('div');
        errorMessage.className = 'error-message';
        errorMessage.textContent = 'Title must be between 5 and 255 characters long.';
        title.classList.add('invalid-field');
        title.parentNode.appendChild(errorMessage);
        isValid = false;
    }

    if (content.value.length < 20) {
        const errorMessage = document.createElement('div');
        errorMessage.className = 'error-message';
        errorMessage.textContent = 'Content must be at least 20 characters long.';
        content.classList.add('invalid-field');
        content.parentNode.appendChild(errorMessage);
        isValid = false;
    }

    if (!gamerate.value) {
        const errorMessage = document.createElement('div');
        errorMessage.className = 'error-message';
        errorMessage.textContent = 'Please select a game rating.';
        gamerate.classList.add('invalid-field');
        gamerate.parentNode.appendChild(errorMessage);
        isValid = false;
    }

    if (!isValid) {
        event.preventDefault();
    }
});
