from django.contrib import admin
from .models import Ingredient, userHistory

# Register your models here.
admin.site.register(Ingredient)
admin.site.register(userHistory)