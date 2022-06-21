from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, render
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, throttle_classes
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate


@require_http_methods(["GET"])
@throttle_classes([])
def home(request):
    context = {}
    return render(request, "home.html", context)


@require_http_methods(["GET"])
@throttle_classes([])
@login_required(login_url="/login")
def panel(request):
    try:
        token = Token.objects.get(user=request.user)
        context = {"token": token}
    except:
        # if user doesn't have an existing token
        context = {}
    return render(request, "panel.html", context)


@require_http_methods(["GET"])
@throttle_classes([])
def docs(request):
    return render(request, "docs.html")


@require_http_methods(["POST"])
@throttle_classes([])
@login_required(login_url="/login")
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


@require_http_methods(["GET"])
@throttle_classes([])
@login_required(login_url="/login")
def create_token(request):
    token = Token.objects.create(user=request.user)
    return redirect(reverse("panel"))


@require_http_methods(["GET"])
@throttle_classes([])
def swagger(request):
    return render(request, "swagger.html")


@require_http_methods(["GET", "POST"])
@throttle_classes([])
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect(reverse("login"))
        else:
            return redirect("signup")
    elif request.method == "GET":
        return render(request, "signup.html", context={"form": UserCreationForm()})