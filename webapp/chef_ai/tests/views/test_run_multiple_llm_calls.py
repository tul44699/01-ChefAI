from django.test import TestCase
from django.urls import reverse


import json
from django.test import TestCase
from django.http import JsonResponse
from asgiref.sync import async_to_sync
from unittest.mock import AsyncMock, patch
from chef_ai.views import run_multiple_llm_calls  # Adjust import

class RunMultipleLLMCallsTest(TestCase):
    @patch('chef_ai.views.feedLLM', new_callable=AsyncMock)
    def test_returns_json_response(self, mock_feed):
        # Setup mock to simulate a recipe response
        mock_feed.return_value = {
            "title": "Test Recipe",
            "cuisine": "Test Cuisine",
            "time": "30 minutes",
            "ingredients": ["2 eggs", "1 cup flour"],
            "utensils": ["pan"],
            "steps": ["Step 1", "Step 2"]
        }

        selected_options = ['egg:2', 'flour:1cup']
        num_recipes = 2

        # Call the coroutine using async_to_sync
        response = async_to_sync(run_multiple_llm_calls)(selected_options, num_recipes)

        # Assert the response is a list of recipes
        data = json.loads(response.content)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), num_recipes)
        
        for recipe in data:
            self.assertIn("title", recipe)
            self.assertIn("cuisine", recipe)
            self.assertIn("time", recipe)
            self.assertIn("ingredients", recipe)
            self.assertIn("utensils", recipe)
            self.assertIn("steps", recipe)
