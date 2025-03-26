from django.db import models

# Create your models here.
class Ingredient(models.Model):
    INGREDIENT_TYPES = [
        ("pantry", "Pantry"),
        ("spice", "Spice"),
        ("protein", "Protein"),
        ("vegetable", "Vegetable"),
        ("dairy", "Dairy"),
        ("grain", "Grain"),
        ("oil", "Oil"),
        ("fruit", "Fruit"),
        ("other", "Other"),
    ]
    
    ingredient_name = models.CharField(max_length=75, blank=False)
    ingredient_type = models.CharField(max_length=50, choices=INGREDIENT_TYPES, default='other')
    