from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, throttle_classes


@api_view(["GET"])
@throttle_classes([])
def home(request):
    context = {}
    return render(request, "home.html", context)


@api_view(["GET"])
@throttle_classes([])
@login_required(login_url="/login")
def panel(request):
    context = {}
    tokens = Token.objects.filter(user=request.user)
    context["tokens"] = tokens
    return render(request, "panel.html", context)


@api_view(["GET"])
@throttle_classes([])
def docs(request):
    return render(request, "docs.html")


@api_view(["POST"])
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


@api_view(["GET"])
@throttle_classes([])
@login_required(login_url="/login")
def create_token(request):
    token = Token.objects.create(user=request.user)
    return redirect(reverse("panel"))


@api_view(["GET"])
@throttle_classes([])
def swagger(request):
    return render(request, "swagger.html")
