from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views

from homepage.views import create_token, delete_token, home, panel, docs

urlpatterns = [
    path("", home, name="home"),
    path("panel/", panel, name="panel"),
    path("docs/", docs, name="docs"),
    path("login/", views.LoginView.as_view(template_name="login.html", next_page="panel"), name="login"),
    path("logout/", views.LogoutView.as_view(next_page="home"), name="logout"),
    path("tokens/delete/", delete_token, name="delete_token"),
    path("tokens/create/", create_token, name="create_token"),
]
