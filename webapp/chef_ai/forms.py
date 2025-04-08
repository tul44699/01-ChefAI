from django import forms
from chef_ai.models import Ingredient
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ingredientList(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    ingredient_types = Ingredient.objects.values_list('ingredient_type',flat=True).distinct()
    
    for type in ingredient_types:
        ingredients = Ingredient.objects.filter(ingredient_type=type)
        
        choices = [(ingredient.ingredient_name, ingredient.ingredient_name) for ingredient in ingredients]
        field_name = f"{type.upper()}"
        locals()[field_name] = forms.MultipleChoiceField(choices = choices, widget=forms.CheckboxSelectMultiple, required=False)
    


class UserRegistration(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        