from django.urls import path, include
from rest_framework import routers
from api.views import CircuitsViewset, ConstructorsViewset, \
    DriversViewset, RacesViewset, SeasonsViewset


# format choice is automatically implemented in router (no need to use format_suffix_patterns())
router = routers.DefaultRouter()
router.register(r"drivers", DriversViewset, basename="driver")
router.register(r"constructors", ConstructorsViewset, basename="constructor")
router.register(r"circuits", CircuitsViewset, basename="circuit")
router.register(r"seasons", SeasonsViewset, basename="season")

races_list = RacesViewset.as_view({"get": "list"})
races_detail = RacesViewset.as_view({"get": "retrieve"})


urlpatterns = [
    path("", include(router.urls)),
    # had to do this to implement multiple fields lookup:
    path("races/<int:year>/<int:round>/", races_detail, name="race-detail"),
    path("races/", races_list, name="race-list"),
]
