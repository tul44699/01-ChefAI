from django.test import TestCase
from django.urls import reverse
from chef_ai.models import Ingredient
from chef_ai.forms import ingredientList
import pytest



class testIngredientListForm(TestCase):
    
    def setUp(self):
        # Simulate the database by adding ingredients to the database
        Ingredient.objects.create(ingredient_name="Tomato", ingredient_type="Vegetable")
        Ingredient.objects.create(ingredient_name="Lettuce", ingredient_type="Vegetable")
        Ingredient.objects.create(ingredient_name="Chicken", ingredient_type="Protein")
        Ingredient.objects.create(ingredient_name="Beef", ingredient_type="Protein")
        Ingredient.objects.create(ingredient_name="Apple", ingredient_type="Fruit")
        
        
    
    def test_get_list_of_choices_from_Table(self):
        # Run the query to get distinct ingredient types
        ingredient_types = Ingredient.objects.values_list('ingredient_type', flat=True).distinct()
        
        # Assert that the distinct ingredient types are correct
        expected_ingredient_types = ['Vegetable', 'Protein', 'Fruit']
        
        # Convert the result to a list and check if it's the same as expected
        self.assertListEqual(list(ingredient_types), expected_ingredient_types)
        print(list(ingredient_types))
    
    @pytest.mark.django_db   
    def test_choices_and_fields_are_dynamic_in_ingredient_list_form(self):

        form = ingredientList()

        # Check that the correct fields were dynamically added
        self.assertIn('VEGETABLE', form.fields)
        self.assertIn('PROTEIN', form.fields)
        self.assertIn('FRUIT', form.fields)

        # Check that choices for a type match what’s in the database
        expected_vegetable_choices = [("Tomato", "Tomato"), ("Lettuce", "Lettuce")]
        self.assertEqual(form.fields['VEGETABLE'].choices, expected_vegetable_choices)

        expected_protein_choices = [("Chicken", "Chicken"), ("Beef", "Beef")]
        self.assertEqual(form.fields['PROTEIN'].choices, expected_protein_choices)