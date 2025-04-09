from django.test import TestCase
from chef_ai.models import Ingredient, userHistory



class IngredientModelTest(TestCase):
    def setUp(self):
        self.ing_name = Ingredient.objects.create(ingredient_name="Orange")
        self.ing_type = Ingredient.objects.create(ingredient_type="fruit")
    
    def test_ingredient_creation(self):
        self.assertEqual(self.ing_name.ingredient_name, "Orange")
        self.assertEqual(self.ing_type.ingredient_type, "fruit")
        self.assertTrue(isinstance(self.ing_name, Ingredient))
        self.assertTrue(isinstance(self.ing_type, Ingredient))
        print("Success test ingredients insert")