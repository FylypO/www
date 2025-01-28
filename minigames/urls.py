from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('games/', views.games, name='games'),
    path('games/<int:pk>/', views.game_site, name='game_site'),
    path('reviews/', views.reviews, name='reviews'),
    path('reviews/<int:pk>/', views.review_site, name='review_site'),
    path('create-review/', views.review_create, name='review_create'),
    path('create-review/<int:game_id>/', views.review_create_id, name='review_create_id'),
    path('create-comment/<str:content_type>/<int:object_id>/', views.comment_create, name='comment_create'),
    path('posts/', views.posts, name='posts'),
    path('posts/<int:pk>/', views.post_site, name='post_site'),
    path('create-post/', views.post_create, name='post_create'),
    path('post/<int:post_id>/edit/', views.PostEditView.as_view(), name='post_edit'),
    path('post/<int:post_id>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    path('profile/', views.profile_redirect, name='profile_redirect'),
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('profile/<int:user_id>/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('profile/<int:user_id>/delete/', views.ProfileDeleteView.as_view(), name='profile_delete'),
    
    path('accounts/', include('allauth.urls')),

    path('post/<int:post_id>/like/', views.PostLikeView.as_view(), name='post_like'),
    path('post/<int:post_id>/dislike/', views.PostDislikeView.as_view(), name='post_dislike'),
    path('post/<int:post_id>/export/', views.export_post_to_pdf, name='export_post_to_pdf'),
    path('post/<int:post_id>/export/xml/', views.export_post_to_xml, name='export_post_to_xml'),

    path('review/<int:review_id>/like/', views.ReviewLikeView.as_view(), name='review_like'),
    path('review/<int:review_id>/dislike/', views.ReviewDislikeView.as_view(), name='review_dislike'),
    path('review/<int:review_id>/edit/', views.ReviewEditView.as_view(), name='review_edit'),
    path('review/<int:review_id>/delete/', views.ReviewDeleteView.as_view(), name='review_delete'),

    path('comment/<int:comment_id>/like/', views.CommentLikeView.as_view(), name='comment_like'),
    path('comment/<int:comment_id>/dislike/', views.CommentDislikeView.as_view(), name='comment_dislike'),
    path('comment/<int:comment_id>/edit/', views.CommentEditView.as_view(), name='comment_edit'),
    path('comment/<int:comment_id>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),

    path('api-posts/', views.api_posts, name='api_posts'),
    path('api/', views.api_page, name='api_page'),
]