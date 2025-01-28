from django import forms
from django.forms import ModelForm
from .models import Review, Comment, Post, Game, Profile
from django.core.exceptions import ValidationError
from datetime import date

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content', 'game', 'gamerate']

    game = forms.ModelChoiceField(queryset=Game.objects.all(), widget=forms.Select)

    def __init__(self, *args, **kwargs):
        game = kwargs.pop('game', None)
        user = kwargs.pop('user', None)
        super(ReviewForm, self).__init__(*args, **kwargs)
        if game or self.instance.pk:
            self.fields['game'].widget.attrs['disabled'] = True
            self.fields['game'].initial = game
        if user:
            self.instance.author = user
        self.fields['gamerate'] = forms.ChoiceField(
            choices=[(i, i) for i in range(5, 0, -1)],
            widget=forms.Select
        )

    def clean_game(self):

        if self.fields['game'].widget.attrs.get('disabled', False):
            game = self.fields['game'].initial
        else:
            game = self.cleaned_data.get('game')
            
        if isinstance(game, Game):
            return game
        try:
            return Game.objects.get(pk=game)
        except Game.DoesNotExist:
            raise forms.ValidationError("Invalid game selection.")

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        if len(title) > 255:
            raise forms.ValidationError("Title must be at most 255 characters long.")
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 20:
            raise forms.ValidationError("Content must be at least 20 characters long.")
        return content

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        content_object = kwargs.pop('content_object', None)
        super(CommentForm, self).__init__(*args, **kwargs)
        if user:
            self.instance.author = user
        if content_object:
            self.instance.content_object = content_object

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > 255:
            raise forms.ValidationError("Comment must be at most 255 characters long.")
        return content

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PostForm, self).__init__(*args, **kwargs)
        if user:
            self.instance.author = user

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > 1500:
            raise forms.ValidationError("Post content must be at most 1500 characters long.")
        return content

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio', 'birth_date', 'location', 'website']

    def clean_website(self):
        website = self.cleaned_data.get('website')
        if website and not website.startswith('http'):
            raise forms.ValidationError("Website URL must start with http or https.")
        return website

    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        if len(bio) > 500:
            raise forms.ValidationError("Bio must be at most 500 characters long.")
        return bio

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date and birth_date < date.today().replace(year=date.today().year - 1115):
            raise forms.ValidationError("Birth date cannot be more than 1115 years ago.")
        return birth_date

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and image.size > 5 * 1024 * 1024:  # 5 MB limit
            raise forms.ValidationError("Image file size must be under 5MB.")
        return image

    def clean_location(self):
        location = self.cleaned_data.get('location')
        if location and len(location) > 255:
            raise forms.ValidationError("Location must be at most 255 characters long.")
        return location