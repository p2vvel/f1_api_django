from django.urls import path
from django.contrib.auth import views
from homepage.views import create_token, delete_token, home, panel, docs, swagger, signup
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view


urlpatterns = [
    path("", home, name="home"),
    path("panel/", panel, name="panel"),
    path("login/", views.LoginView.as_view(template_name="login.html", next_page="panel"), name="login"),
    path("signup/", signup, name="signup"),
    path("logout/", views.LogoutView.as_view(next_page="home"), name="logout"),
    path("tokens/delete/", delete_token, name="delete_token"),
    path("tokens/create/", create_token, name="create_token"),
    path('docs/', TemplateView.as_view(template_name='swagger.html'), name='docs'),
    path('schema/', get_schema_view(title="F1 API", description="F1 API build using DRF and Ergast DB dumps"), name="openapi_schema"),

]
