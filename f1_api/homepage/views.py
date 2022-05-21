from django.shortcuts import redirect, render
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.conf import settings



@require_http_methods(["GET"])
def home(request):
    context = {}
    return render(request, "home.html", context)


@require_http_methods(["GET"])
@login_required(login_url="/login")
def panel(request):
    context = {}
    tokens = Token.objects.filter(user=request.user)
    context["tokens"] = tokens
    return render(request, "panel.html", context)


@require_http_methods(["GET"])
def docs(request):
    return render(request, "docs.html")


@login_required(login_url="/login")
@require_http_methods(["POST"])
def delete_token(request):
    try:
        token_pk = request.POST.get("token_pk", None)
        assert token_pk is not None, "Token has not been sent in the request!"
        # fetch token from DB
        token = Token.objects.get(pk=token_pk)
        # check if user is owner of the token
        assert token.user == request.user, "You are not the owner!"  
        # user is owner, delete it
        token.delete()
        return redirect(reverse("panel"))
    except:
        return redirect(reverse("home"))


@login_required(login_url="/login")
@require_http_methods(["GET"])
def create_token(request):
    token = Token.objects.create(user=request.user)
    return redirect(reverse("panel"))


@require_http_methods(["GET"])
def swagger(request):
    return render(request, "swagger.html")