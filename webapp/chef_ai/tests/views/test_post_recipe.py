from django.test import TestCase, Client
from django.urls import reverse
from django import forms
from chef_ai.forms import UserRegistration
from django.contrib.auth.models import User
from chef_ai.views import feedLLM
from chef_ai.models import userHistory
import json

class postRecipeViewTest(TestCase):
    
    def test_post_recipe_view_status_code_no_post_request(self):
        response = self.client.get(reverse('post-recipe'))
        self.assertEqual(response.status_code, 400)
        


    def test_post_recipe(self):
        client = Client(enforce_csrf_checks=True)
        
        response = client.get(reverse('index'))  # or any page that sets the CSRF cookie
        csrftoken = client.cookies['csrftoken'].value
        data = {
            'ingredients': ['egg', 'flour'],
            'numberOfRecipes': 1
        }
        response = client.post(
            '/post-recipe/',
            data=json.dumps(data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            HTTP_X_CSRFTOKEN=csrftoken 
        )
        results = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(results['status'], "success")


    def test_post_recipe_view_form_post_has_one_ingredient(self):
        client = Client(enforce_csrf_checks=True)
        
        response = client.get(reverse('index'))  # or any page that sets the CSRF cookie
        csrftoken = client.cookies['csrftoken'].value
        data = {
            'ingredients': ['egg'],
            'numberOfRecipes': 1
        }
        response = client.post(
            '/post-recipe/',
            data=json.dumps(data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            HTTP_X_CSRFTOKEN=csrftoken 
        )
        results = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(results['status'], "success")
        
    def test_post_recipe_view_form_post_has_one_ingredient_with_qty(self):
        
        client = Client(enforce_csrf_checks=True)
        
        response = client.get(reverse('index'))  # or any page that sets the CSRF cookie
        csrftoken = client.cookies['csrftoken'].value
        data = {
            'ingredients': ['egg:2'],
            'numberOfRecipes': 1
        }
        response = client.post(
            '/post-recipe/',
            data=json.dumps(data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            HTTP_X_CSRFTOKEN=csrftoken 
        )
        results = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(results['status'], "success")
    
    
    def test_post_recipe_view_form_post_has_many_ingredients(self):
        client = Client(enforce_csrf_checks=True)
        
        response = client.get(reverse('index'))  # or any page that sets the CSRF cookie
        csrftoken = client.cookies['csrftoken'].value
        data = {
            'ingredients': ['egg', 'bacon', 'hamburger', 'cheese', 'bread', 'salt'],
            'numberOfRecipes': 1
        }
        response = client.post(
            '/post-recipe/',
            data=json.dumps(data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            HTTP_X_CSRFTOKEN=csrftoken 
        )
        results = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(results['status'], "success")
        
    def test_post_recipe_view_form_post_has_many_ingredients_and_amounts(self):
        client = Client(enforce_csrf_checks=True)
        
        response = client.get(reverse('index'))  # or any page that sets the CSRF cookie
        csrftoken = client.cookies['csrftoken'].value
        data = {
            'ingredients': ['egg:2', 'bacon:5 slices', 'hamburger:8oz', 'cheese:1lb', 'bread:1 loaf', 'salt:alot'],
            'numberOfRecipes': 1
        }
        response = client.post(
            '/post-recipe/',
            data=json.dumps(data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            HTTP_X_CSRFTOKEN=csrftoken 
        )
        results = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(results['status'], "success")
        
        
    def test_post_recipe_view_form_post_has_many_ingredients_and_amounts_and_many_recipes(self):
        client = Client(enforce_csrf_checks=True)
        
        response = client.get(reverse('index'))  # or any page that sets the CSRF cookie
        csrftoken = client.cookies['csrftoken'].value
        data = {
            'ingredients': ['egg:2', 'bacon:5 slices', 'hamburger:8oz', 'cheese:1lb', 'bread:1 loaf', 'salt:alot'],
            'numberOfRecipes': 3
        }
        response = client.post(
            '/post-recipe/',
            data=json.dumps(data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            HTTP_X_CSRFTOKEN=csrftoken 
        )
        results = response.json()
    
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(results['status'], "success")
    
    def test_post_recipe_data_saved_in_session(self):

        client = Client(enforce_csrf_checks=True)
        
        response = client.get(reverse('index'))  # or any page that sets the CSRF cookie
        csrftoken = client.cookies['csrftoken'].value
        data = {
            'ingredients': ['egg:2'],
            'numberOfRecipes': 1
        }
        response = client.post(
            '/post-recipe/',
            data=json.dumps(data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            HTTP_X_CSRFTOKEN=csrftoken 
        )
        session = client.session
        
        self.assertIn('ai_response', session)
       
      
  
    def test_user_history_gets_saved(self):
        self.client = Client(enforce_csrf_checks=True)
        
        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testing1234')
        
        login = self.client.login(username='testuser', password='testing1234')
        self.assertTrue(login)
        
        
        
        response = self.client.get(reverse('index'))  # or any page that sets the CSRF cookie
        csrftoken = self.client.cookies['csrftoken'].value
        data = {
            'ingredients': ['egg:2'],
            'numberOfRecipes': 1
        }
        response = self.client.post(
            '/post-recipe/',
            data=json.dumps(data),
            content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
            HTTP_X_CSRFTOKEN=csrftoken 
        )
   
        self.assertEqual(response.status_code, 200)
        history = userHistory.objects.filter(userID=user).first()
        self.assertIsNotNone(history)

        self.assertEqual(history.selectedIngredients, "egg:2")