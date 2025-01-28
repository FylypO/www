from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

class Game(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    studio = models.CharField(max_length=255)
    release_date = models.DateField()
    image = models.ImageField(upload_to='games/', null=True, blank=True, default='media/deault_profile.png')

    def __str__(self):
        return self.title

class ReactionMixin(models.Model):
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    reactions = GenericRelation('Reaction', related_query_name='content_object')

    class Meta:
        abstract = True

    @property
    def like_count(self):
        return self.reactions.filter(reaction_type=Reaction.ReactionType.LIKE).count()

    @property
    def dislike_count(self):
        return self.reactions.filter(reaction_type=Reaction.ReactionType.DISLIKE).count()

    def add_like(self, user):
        self.reactions.create(
            created_by=user,
            reaction_type=Reaction.ReactionType.LIKE,
            updated_by=user,
        )

    def add_dislike(self, user):
        self.reactions.create(
            created_by=user,
            reaction_type=Reaction.ReactionType.DISLIKE,
            updated_by=user,
        )

    def delete_like(self, user):
        self.reactions.filter(reaction_type=Reaction.ReactionType.LIKE, created_by=user).delete()

    def delete_dislike(self, user):
        self.reactions.filter(reaction_type=Reaction.ReactionType.DISLIKE, created_by=user).delete()

    def has_liked(self, user):
        return (user.is_authenticated 
                and self.reactions.filter(created_by=user, reaction_type=Reaction.ReactionType.LIKE).exists())

    def has_disliked(self, user):
        return (user.is_authenticated 
                and self.reactions.filter(created_by=user, reaction_type=Reaction.ReactionType.DISLIKE).exists())

class Post(ReactionMixin, models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    edited = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('post_site', args=[str(self.id)])

    def change_edit_flag(self):
        self.edited = True
        self.updated_at = models.DateTimeField(auto_now=True)
        self.save()

    def delete_post(self):
        self.delete()

    def __str__(self):
        return self.content[0:10]

class Comment(ReactionMixin, models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    edited = models.BooleanField(default=False)

    def change_edit_flag(self):
        self.edited = True
        self.updated_at = models.DateTimeField(auto_now=True)
        self.save()

    def delete_comment(self):
        self.delete()

class Review(ReactionMixin, models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    gamerate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    edited = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('review_site', args=[str(self.id)])

    def change_edit_flag(self):
        self.edited = True
        self.updated_at = models.DateTimeField(auto_now=True)
        self.save()

    def delete_review(self):
        self.delete()

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profiles/', null=True, blank=True, default='media/default_profile.png')
    bio = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Reaction(models.Model):

    class ReactionType(models.TextChoices):
        LIKE = "like", "Like"
        DISLIKE = "dislike", "Dislike"

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='reactions')
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    reaction_type = models.CharField(max_length=10, choices=ReactionType.choices)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_reactions')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_reactions')