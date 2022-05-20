from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views

from homepage.views import home, panel, docs

urlpatterns = [
    # path('/', ),
    path("", home, name="home"),
    path("panel/", panel, name="panel"),
    path("docs/", docs, name="docs"),
    path("login/", views.LoginView.as_view(template_name="login.html", next_page="panel"), name="login"),
    path("logout/", views.LogoutView.as_view(next_page="home"), name="logout"),
    # path("logout/", views.LogoutView.as_view(), name="login"),

]
