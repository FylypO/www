from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Game, Post, Review, Comment

class MinigamesTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.game = Game.objects.create(title='Test Game', release_date='2025-01-01')
        self.post = Post.objects.create(content='Test Content', author=self.user)
        self.review = Review.objects.create(title='Test Review', content='Test Content', author=self.user, game=self.game, gamerate=5)
        self.comment = Comment.objects.create(content='Test Comment', author=self.user, content_object=self.review)

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'minigames/home.html')

    def test_games_view(self):
        response = self.client.get(reverse('games'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'minigames/games.html')

    def test_game_site_view(self):
        response = self.client.get(reverse('game_site', args=[self.game.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'minigames/game_site.html')

    def test_reviews_view(self):
        response = self.client.get(reverse('reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'minigames/reviews.html')

    def test_review_site_view(self):
        response = self.client.get(reverse('review_site', args=[self.review.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'minigames/review_site.html')

    def test_posts_view(self):
        response = self.client.get(reverse('posts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'minigames/posts.html')

    def test_post_site_view(self):
        response = self.client.get(reverse('post_site', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'minigames/post_site.html')

    def test_user_profile_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('user_profile', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'minigames/user_profile.html')

    def test_review_create_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('review_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'minigames/review_form.html')

    def test_post_create_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'minigames/post_form.html')

    def test_comment_create_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('comment_create', args=['review', self.review.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'minigames/comment_form.html')
