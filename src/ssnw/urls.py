from flask import current_app
from . import views

app = current_app

rules = [
    ('/', views.home.HomeView.as_view('home')),
    ('/users/', views.user.UserView.as_view('users')),
    ('/users/signup', views.user.SignupView.as_view('signup')),
    ('/users/login', views.user.LoginView.as_view('login')),
]

for url, view_func in rules:
    app.add_url_rule(url, view_func=view_func)
