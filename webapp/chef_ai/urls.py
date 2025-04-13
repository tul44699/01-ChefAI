from django.urls import path
from . import views


urlpatterns = [
    path("", views.landing, name="landing"),
    path("home/", views.index, name="index"),
    path("test/", views.index, name="test"),
    path("recipe/", views.list_of_recipes, name="response_recipe"),
    path("download-pdf/", views.download_pdf, name = 'download_pdf'),
    path("download-jpg/", views.download_jpg, name='download_jpg'),
    path("search/", views.search_ingredients, name="search_ingredients"),
    path('register/', views.userRegistration, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('profile/', views.getProfile, name='profile'),
    path('scan-images/', views.scan_images, name='scan-images'),
    path('history/<int:recipe_id>/', views.view_saved_recipe, name='view_saved_recipe'),
    path('post-recipe/', views.post_recipe, name="post-recipe"),
]