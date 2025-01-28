function handleAction(itemType, itemId, action) {
    const url = `/${itemType}/${itemId}/${action}/`;

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
    })
        .then(response => response.json())
        .then(data => {
            const likesCount = document.querySelector(`#${itemType}-${itemId}-likes`);
            const dislikesCount = document.querySelector(`#${itemType}-${itemId}-dislikes`);

            if (likesCount && dislikesCount) {
                likesCount.textContent = `Likes: ${data.like_count}`;
                dislikesCount.textContent = `Dislikes: ${data.dislike_count}`;
            }

            const likeButton = document.querySelector(`.like-button[data-id="${itemId}"][data-type="${itemType}"]`);
            const dislikeButton = document.querySelector(`.dislike-button[data-id="${itemId}"][data-type="${itemType}"]`);

            if (likeButton && dislikeButton) {
                if (data.liked) {
                    likeButton.classList.add('active');
                    likeButton.textContent = 'Liked';
                    dislikeButton.classList.remove('active');
                    dislikeButton.textContent = 'Dislike';
                } else if (data.disliked) {
                    likeButton.classList.remove('active');
                    likeButton.textContent = 'Like';
                    dislikeButton.classList.add('active');
                    dislikeButton.textContent = 'Disliked';
                } else {
                    likeButton.classList.remove('active');
                    likeButton.textContent = 'Like';
                    dislikeButton.classList.remove('active');
                    dislikeButton.textContent = 'Dislike';
                }
            }
        })
        .catch(error => console.error('Error:', error));
}

function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    return '';
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.like-button').forEach(button => {
        button.addEventListener('click', () => {
            const itemId = button.dataset.id;
            const itemType = button.dataset.type;
            handleAction(itemType, itemId, 'like');
        });
    });

    document.querySelectorAll('.dislike-button').forEach(button => {
        button.addEventListener('click', () => {
            const itemId = button.dataset.id;
            const itemType = button.dataset.type;
            handleAction(itemType, itemId, 'dislike');
        });
    });
});