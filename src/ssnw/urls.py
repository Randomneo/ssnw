from flask import current_app
from . import views

app = current_app

rules = [
    ('/', views.home.HomeView.as_view('home')),
    ('/users/', views.user.UserListView.as_view('users')),
    ('/users/signup', views.user.SignupView.as_view('signup')),
    ('/users/login', views.user.LoginView.as_view('login')),
    ('/posts/', views.post.PostListView.as_view('posts')),
    ('/posts/<int:id>/', views.post.PostDetailView.as_view('post_detail')),
    ('/posts/<int:post_id>/like/', views.like.LikePostView.as_view('like_post')),
    ('/posts/<int:post_id>/dislike/', views.like.DisLikePostView.as_view('dislike_post')),
    ('/likes/', views.like.LikeListView.as_view('like')),
]

for url, view_func in rules:
    app.add_url_rule(url, view_func=view_func)
