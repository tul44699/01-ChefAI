from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Ingredient(models.Model):
    
    ingredient_name = models.CharField(max_length=75, unique=True, blank=False)
    ingredient_type = models.CharField(max_length=50, default='other')
    

class userHistory(models.Model):
    userID = models.ForeignKey(User, on_delete = models.PROTECT)
    selectedIngredients = models.CharField(max_length=2000, blank=False)
    generatedRecipe = models.CharField(max_length=10000, blank=False)
    title = models.CharField(max_length=255, default='Untitled Recipe')
