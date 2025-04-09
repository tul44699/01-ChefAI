from django.test import TestCase
from django.urls import reverse
from django import forms
from chef_ai.forms import UserRegistration
from django.contrib.auth.models import User
from chef_ai.views import feedLLM
from chef_ai.models import userHistory
# Create your tests here.


class IndexViewTest(TestCase):
    

    def test_index_view_status_code(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)


    def test_index_view_form_post_isEmpty(self):
        response = self.client.post(reverse('index'), {'final_ingredients':""})
        self.assertEqual(response.status_code, 302)


    def test_index_view_form_post_has_one_ingredient(self):
        response = self.client.post(reverse('index'), {"final_ingredients":"Rice"})
        self.assertEqual(response.status_code, 302)
        
    def test_index_view_form_post_has_one_ingredient_with_qty(self):
        response = self.client.post(reverse('index'),{"final_ingredients": "Rice {1cup}"})
        self.assertEqual(response.status_code, 302)
    
    
    def test_index_view_form_post_has_many_ingredients(self):
        response = self.client.post(reverse('index'), {"final_ingredients":"Rice, Apple, Sugar, Steak"})
        self.assertEqual(response.status_code, 302)
        
    def test_index_view_form_post_has_many_ingredients_and_amounts(self):
        response = self.client.post(reverse('index'), {"final_ingredients":"Rice (1), Apple (1), Sugar(1 cup), Steak (12oz)"})
        self.assertEqual(response.status_code, 302)
    
    def test_index_data_saved_in_session(self):
        data = {'final_ingredients':'Rice {1 cup}'}

        response = self.client.post(reverse('index'), data)

        session = self.client.session

        self.assertIn('selected_options', session)
        self.assertIn('ai_response', session)
       
      
  
    def test_user_history_gets_saved(self):

        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testing1234')
        
        login = self.client.login(username='testuser', password='testing1234')
        self.assertTrue(login)
        selected_options = 'Tomato, Lettuce, Bacon'
        response = self.client.post(reverse('index'), {'final_ingredients':selected_options})
        
        self.assertEqual(response.status_code, 302)
        history = userHistory.objects.filter(userID=self.user).first()
        self.assertIsNotNone(history)
        print(f"Ingredients in table {history.selectedIngredients}")

        self.assertEqual(history.selectedIngredients, selected_options)
        
        
        
        
        