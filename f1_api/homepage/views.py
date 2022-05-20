from django.shortcuts import render

# Create your views here.


def home(request):
    context = {}
    return render(request, "home.html", context)

def panel(request):
    context = {}
    return render(request, "panel.html", context)

def docs(request):
    context = {}
    return render(request, "docs.html", context)