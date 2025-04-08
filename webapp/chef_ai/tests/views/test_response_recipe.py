from django.test import TestCase
from django.urls import reverse


class response_recipeTest(TestCase):
    
    
    def test_get_response_from_session(self):
        session = self.client.session
        session['selected_options'] = ['option1', 'option2']
        session['ai_response'] = 'Here is the AI-generated recipe'
        session.save()

        # Now send the request
        response = self.client.get(reverse('response_recipe'))

        # Ensure correct response
        self.assertEqual(response.status_code, 200)

        # Confirm context contains expected data
        self.assertIn('selected_options', response.context)
        self.assertIn('ai_response', response.context)

        self.assertEqual(response.context['selected_options'], ['option1', 'option2'])
        self.assertEqual(response.context['ai_response'], 'Here is the AI-generated recipe')

        
    def test_response_recipe_without_session_data(self):
        # Send a GET request to the response_recipe view without setting session data
        response = self.client.get(reverse('response_recipe'))  # Replace with the correct URL name

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the context variables are set to default values
        self.assertIn('selected_options', response.context)
        self.assertIn('ai_response', response.context)

        self.assertEqual(response.context['selected_options'], [])
        self.assertEqual(response.context['ai_response'], "")