from django.test import TestCase
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.http import FileResponse


class DownloadJPGTest(TestCase):
    
    def setUp(self):
        # Mock data to be used for the ai_response
        self.ai_response = [{
            'title': 'Delicious Pasta',
            'cuisine': 'Italian',
            'ingredients': ['Pasta', 'Tomato Sauce', 'Basil'],
            'steps': ['Boil pasta', 'Prepare sauce', 'Combine and serve']
        }]
        # self.ai_response=[{'title': 'Simple Spice Blend', 'cuisine': 'American', 'time': '5 minutes', 'ingredients': ['Paprika : 1', 'Black Pepper : 1', 'Oregano : 1', 'Turmeric : 1'], 'utensils': ['Small bowl', 'Spoon'], 'steps': ['In a small bowl, combine the Paprika, Black Pepper, Oregano, and Turmeric.', 'Mix the spices together using a spoon until they are well combined.', 'Your simple spice blend is now ready to use as a seasoning for various dishes.', 'Note: This recipe is a basic spice blend that can be used to add flavor to a variety of dishes, such as soups, salads, or meats. You can store the blend in an airtight container for later use.']}]
        # Set the session data
        self.client.session['ai_response'] = self.ai_response
        self.client.session.save()

    def test_download_jpg_no_ai_response(self):
        # Simulate that the session doesn't contain 'ai_response'
        response = self.client.get(reverse('download_jpg'))
        
        # The response should be a redirect to the 'response_recipe' page
        self.assertRedirects(response, reverse('response_recipe'))

    def test_download_jpg_with_ai_response(self):
        
        session = self.client.session
        session['ai_response'] = self.ai_response
        session.save()
        
        response = self.client.get(reverse('download_jpg'))
        print(f"Response type: {type(response)}")
        
        self.assertIsInstance(response, FileResponse)