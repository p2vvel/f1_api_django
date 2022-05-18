"""f1_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api.views import CircuitsViewset, ConstructorsViewset, DriversViewset, RacesViewset, SeasonsViewset

# format choice is automatically implemented in router (no need to use format_suffix_patterns())
router = routers.DefaultRouter()
router.register(r"drivers", DriversViewset, basename="driver")
router.register(r"constructors", ConstructorsViewset, basename="constructor")
router.register(r"circuits", CircuitsViewset, basename="circuit")
router.register(r"seasons", SeasonsViewset, basename="season")
# router.register(r"races", RacesViewset, basename="race")
# router.register(r"resource/(?P<year>[0-9]{,4})/(?P<round>[0-9]{,2})", RacesViewset, basename="race")

races_list = RacesViewset.as_view({"get": "list"})
races_detail = RacesViewset.as_view({"get": "retrieve"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
    # had to do this to implement multiple fields lookup:
    path("api/races/<int:year>/<int:round>/", races_detail, name="race-detail"),
    path("api/races/", races_list, name="race-list"),
]
