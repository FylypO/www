from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import JsonResponse, HttpResponse
from .models import Game, Post, Review, Comment
from .forms import ReviewForm, CommentForm, PostForm, ProfileForm
from django.contrib.contenttypes.models import ContentType
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import xml.etree.ElementTree as ET


def home(request):
    context = {'reviews': Review.objects.all().order_by('-likes'), 'posts': Post.objects.all().order_by('-likes')}
    return render(request, 'minigames/home.html', context)



def games(request):
    games = Game.objects.all().order_by('-release_date')
    context = {"games": games}
    return render(request, 'minigames/games.html', context)

def game_site(request, pk):
    game = Game.objects.get(pk=pk)
    context = {'game': game}
    return render(request, 'minigames/game_site.html', context)



def reviews(request):
    reviews = Review.objects.all().order_by('-created_at')
    context = {"reviews": reviews}
    return render(request, 'minigames/reviews.html', context)

def review_site(request, pk):
    comments = Comment.objects.filter(content_type__model='review', object_id=pk).order_by('-created_at')
    review = Review.objects.get(pk=pk)
    context = {
        'review': review,
        'comments': comments,
        'user': request.user,
    }
    return render(request, 'minigames/review_site.html', context)

def review_create(request):
    user = request.user
    redirect_url = request.GET.get('next', 'profile')
    form = ReviewForm(user=user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, user=user)
        if form.is_valid():
            review = form.save()
            return redirect('review_site', pk=review.pk)
    context = {'form': form, 'user': user, 'redirect_url': redirect_url}
    return render(request, 'minigames/review_form.html', context)

def review_create_id(request, game_id):
    game = Game.objects.get(pk=game_id)
    user = request.user
    redirect_url = request.GET.get('next', 'game_site')
    form = ReviewForm(game=game, user=user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, game=game, user=user)
        if form.is_valid():
            review = form.save()
            return redirect('review_site', pk=review.pk)
    context = {'form': form, 'game': game, 'user': user, 'redirect_url': redirect_url}
    print(request.POST)
    return render(request, 'minigames/review_form.html', context)

def posts(request):
    posts = Post.objects.all().order_by('-created_at')
    context = {"posts": posts}
    return render(request, 'minigames/posts.html', context)

def post_site(request, pk):
    comments = Comment.objects.filter(content_type__model='post', object_id=pk).order_by('-created_at')
    post = Post.objects.get(pk=pk)
    context = {
        'post': post,
        'comments': comments,
        'user': request.user,
    }
    return render(request, 'minigames/post_site.html', context)

def post_create(request):
    user = request.user
    form = PostForm(user=user)
    if request.method == 'POST':
        form = PostForm(request.POST, user=user)
        if form.is_valid():
            form.save()
            return redirect('posts')
    context = {'form': form, 'user': user}
    return render(request, 'minigames/post_form.html', context)

class PostEditView(LoginRequiredMixin, View):
    """View for editing a post."""

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if post.author != request.user:
            return redirect(post.get_absolute_url())
        form = PostForm(instance=post)
        return render(request, 'minigames/post_form.html', {'form': form})

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if post.author != request.user:
            return redirect(post.get_absolute_url())
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.change_edit_flag()
            return redirect(post.get_absolute_url())
        return render(request, 'minigames/post_form.html', {'form': form})

class PostDeleteView(LoginRequiredMixin, View):
    """View for deleting a post."""

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if post.author == request.user:
            post.delete_post()
        return redirect('posts')


def about(request):
    return render(request, 'minigames/about.html')

@login_required
def profile_redirect(request):
    return redirect('user_profile', user_id=request.user.id)

@login_required
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'minigames/user_profile.html', {'profile_user': user})

def comment_create(request, content_type, object_id):
    user = request.user
    content_type = get_object_or_404(ContentType, model=content_type)
    content_object = get_object_or_404(content_type.model_class(), id=object_id)
    form = CommentForm(user=user, content_object=content_object)
    if request.method == 'POST':
        form = CommentForm(request.POST, user=user, content_object=content_object)
        if form.is_valid():
            form.save()
            return redirect(content_object.get_absolute_url())
    context = {'form': form, 'user': user, 'content_object': content_object}
    return render(request, 'minigames/comment_form.html', context)

class ReviewActionView(LoginRequiredMixin, View):
    """Base class to handle liking and disliking a review."""

    def get_review(self, review_id):
        """Retrieve the review object or return a 404 error if not found."""
        return get_object_or_404(Review, id=review_id)

    def toggle_like(self, review, user):
        """Toggle the like status for a review."""
        if review.has_liked(user):
            review.delete_like(user)
            return False
        else:
            review.add_like(user)
            return True

    def toggle_dislike(self, review, user):
        """Toggle the dislike status for a review."""
        if review.has_disliked(user):
            review.delete_dislike(user)
            return False
        else:
            review.add_dislike(user)
            return True


class LikeView(ReviewActionView):
    """View for liking a review."""

    def post(self, request, review_id):
        review = self.get_review(review_id)
        disliked = review.has_disliked(request.user)

        if disliked:
            review.delete_dislike(request.user)

        liked = self.toggle_like(review, request.user)

        return JsonResponse(
            {
                "liked": liked,
                "like_count": review.like_count,
                "dislike_count": review.dislike_count,
            }
        )


class DislikeView(ReviewActionView):
    """View for disliking a review."""

    def post(self, request, review_id):
        review = self.get_review(review_id)
        liked = review.has_liked(request.user)

        if liked:
            review.delete_like(request.user)

        disliked = self.toggle_dislike(review, request.user)

        return JsonResponse(
            {
                "disliked": disliked,
                "like_count": review.like_count,
                "dislike_count": review.dislike_count,
            }
        )

class ReactionActionView(View):
    """Base class to handle liking and disliking content."""

    def get_object(self, model, object_id):
        """Retrieve the object or return a 404 error if not found."""
        return get_object_or_404(model, id=object_id)

    def toggle_like(self, obj, user):
        """Toggle the like status for an object."""
        if obj.has_liked(user):
            obj.delete_like(user)
            return False
        else:
            obj.add_like(user)
            return True

    def toggle_dislike(self, obj, user):
        """Toggle the dislike status for an object."""
        if obj.has_disliked(user):
            obj.delete_dislike(user)
            return False
        else:
            obj.add_dislike(user)
            return True

class PostLikeView(ReactionActionView):
    """View for liking a post."""

    def post(self, request, post_id):
        post = self.get_object(Post, post_id)
        disliked = post.has_disliked(request.user)

        if disliked:
            post.delete_dislike(request.user)

        liked = self.toggle_like(post, request.user)

        return JsonResponse(
            {
                "liked": liked,
                "like_count": post.like_count,
                "dislike_count": post.dislike_count,
            }
        )

class PostDislikeView(ReactionActionView):
    """View for disliking a post."""

    def post(self, request, post_id):
        post = self.get_object(Post, post_id)
        liked = post.has_liked(request.user)

        if liked:
            post.delete_like(request.user)

        disliked = self.toggle_dislike(post, request.user)

        return JsonResponse(
            {
                "disliked": disliked,
                "like_count": post.like_count,
                "dislike_count": post.dislike_count,
            }
        )

class ReviewLikeView(ReactionActionView):
    """View for liking a review."""

    def post(self, request, review_id):
        review = self.get_object(Review, review_id)
        disliked = review.has_disliked(request.user)

        if disliked:
            review.delete_dislike(request.user)

        liked = self.toggle_like(review, request.user)

        return JsonResponse(
            {
                "liked": liked,
                "like_count": review.like_count,
                "dislike_count": review.dislike_count,
            }
        )

class ReviewDislikeView(ReactionActionView):
    """View for disliking a review."""

    def post(self, request, review_id):
        review = self.get_object(Review, review_id)
        liked = review.has_liked(request.user)

        if liked:
            review.delete_like(request.user)

        disliked = self.toggle_dislike(review, request.user)

        return JsonResponse(
            {
                "disliked": disliked,
                "like_count": review.like_count,
                "dislike_count": review.dislike_count,
            }
        )

class CommentLikeView(ReactionActionView):
    """View for liking a comment."""

    def post(self, request, comment_id):
        comment = self.get_object(Comment, comment_id)
        disliked = comment.has_disliked(request.user)

        if disliked:
            comment.delete_dislike(request.user)

        liked = self.toggle_like(comment, request.user)

        return JsonResponse(
            {
                "liked": liked,
                "like_count": comment.like_count,
                "dislike_count": comment.dislike_count,
            }
        )

class CommentDislikeView(ReactionActionView):
    """View for disliking a comment."""

    def post(self, request, comment_id):
        comment = self.get_object(Comment, comment_id)
        liked = comment.has_liked(request.user)

        if liked:
            comment.delete_like(request.user)

        disliked = self.toggle_dislike(comment, request.user)

        return JsonResponse(
            {
                "disliked": disliked,
                "like_count": comment.like_count,
                "dislike_count": comment.dislike_count,
            }
        )

class CommentEditView(LoginRequiredMixin, View):

    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.author != request.user:
            return redirect(comment.content_object.get_absolute_url())
        form = CommentForm(instance=comment)
        return render(request, 'minigames/comment_form.html', {'form': form})

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.author != request.user:
            return redirect(comment.content_object.get_absolute_url())
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.change_edit_flag()
            return redirect(comment.content_object.get_absolute_url())
        return render(request, 'minigames/comment_form.html', {'form': form})

class ReviewEditView(LoginRequiredMixin, View):

    def get(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        if review.author != request.user:
            return redirect(review.get_absolute_url())
        form = ReviewForm(instance=review)
        return render(request, 'minigames/review_form.html', {'form': form})

    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        if review.author != request.user:
            return redirect(review.get_absolute_url())
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.change_edit_flag()
            return redirect(review.get_absolute_url())
        return render(request, 'minigames/review_form.html', {'form': form})
    
class ProfileEditView(LoginRequiredMixin, View):
    
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if user != request.user:
            return redirect('user_profile', user_id=user.id)
        form = ProfileForm(instance=user.profile)
        return render(request, 'minigames/edit_profile.html', {'form': form})

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if user != request.user:
            return redirect('user_profile', user_id=user.id)
        form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile', user_id=user.id)
        return render(request, 'minigames/edit_profile.html', {'form': form})

class CommentDeleteView(LoginRequiredMixin, View):
    """View for deleting a comment."""

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.author == request.user:
            comment.delete_comment()
        return redirect(comment.content_object.get_absolute_url())

class ReviewDeleteView(LoginRequiredMixin, View):
    """View for deleting a review."""

    def post(self, request, review_id):
        review = get_object_or_404(Review, id=review_id)
        if review.author == request.user:
            review.delete_review()
        return redirect('reviews')
    
class ProfileDeleteView(LoginRequiredMixin, View):
    """View for deleting a profile."""

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if user == request.user:
            user.delete()
        return redirect('home')

def export_post_to_pdf(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(content_type__model='post', object_id=post_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="post_{post_id}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    p.drawString(100, height - 100, f"Post ID: {post.id}")
    p.drawString(100, height - 120, f"Author: {post.author.username}")
    p.drawString(100, height - 140, f"Created at: {post.created_at}")
    p.drawString(100, height - 160, f"Updated at: {post.updated_at}")
    p.drawString(100, height - 180, f"Content: {post.content}")

    y_position = height - 220
    for comment in comments:
        p.drawString(100, y_position, f"Comment by: {comment.author.username}")
        y_position -= 20
        p.drawString(100, y_position, f"Created at: {comment.created_at}")
        y_position -= 20
        p.drawString(100, y_position, f"Updated at: {comment.updated_at}")
        y_position -= 20
        p.drawString(100, y_position, f"Content: {comment.content}")
        y_position -= 40

    p.showPage()
    p.save()

    return response

def generate_pdf(request, review_id):
    # Get the review and its comments
    review = Review.objects.get(id=review_id)
    comments = Comment.objects.filter(review=review)

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="review_{review_id}.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Draw the review details
    p.drawString(100, height - 100, f"Title: {review.title}")
    p.drawString(100, height - 120, f"Author: {review.author.username}")
    p.drawString(100, height - 140, f"Created at: {review.created_at}")
    p.drawString(100, height - 160, f"Updated at: {review.updated_at}")
    p.drawString(100, height - 180, f"Content: {review.content}")

    # Draw the comments
    y_position = height - 220
    for comment in comments:
        p.drawString(100, y_position, f"Comment by: {comment.author.username}")
        y_position -= 20
        p.drawString(100, y_position, f"Created at: {comment.created_at}")
        y_position -= 20
        p.drawString(100, y_position, f"Updated at: {comment.updated_at}")
        y_position -= 20
        p.drawString(100, y_position, f"Content: {comment.content}")
        y_position -= 40

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    return response

def export_post_to_xml(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(content_type__model='post', object_id=post_id)

    root = ET.Element("post")
    ET.SubElement(root, "id").text = str(post.id)
    ET.SubElement(root, "author").text = post.author.username
    ET.SubElement(root, "created_at").text = str(post.created_at)
    ET.SubElement(root, "updated_at").text = str(post.updated_at)
    ET.SubElement(root, "content").text = post.content

    comments_element = ET.SubElement(root, "comments")
    for comment in comments:
        comment_element = ET.SubElement(comments_element, "comment")
        ET.SubElement(comment_element, "author").text = comment.author.username
        ET.SubElement(comment_element, "created_at").text = str(comment.created_at)
        ET.SubElement(comment_element, "updated_at").text = str(comment.updated_at)
        ET.SubElement(comment_element, "content").text = comment.content

    tree = ET.ElementTree(root)
    response = HttpResponse(content_type='application/xml')
    response['Content-Disposition'] = f'attachment; filename="post_{post_id}.xml"'
    tree.write(response, encoding='utf-8', xml_declaration=True)

    return response

def api_posts(request):
    posts = Post.objects.all().order_by('-created_at')
    data = []
    for post in posts:
        data.append({
            'id': post.id,
            'author': post.author.username,
            'created_at': post.created_at,
            'updated_at': post.updated_at,
            'content': post.content,
            'like_count': post.like_count,
            'dislike_count': post.dislike_count,
        })
    return JsonResponse(data, safe=False)

def api_page(request):
    return render(request, 'minigames/api_page.html')