from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("test/", views.index, name="test"),
    path("recipe/", views.response_recipe, name="response_recipe"),


]