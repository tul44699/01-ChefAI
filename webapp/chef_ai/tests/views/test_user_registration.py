import pytest
from django.urls import reverse
from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


@pytest.mark.django_db
class UserRegistrationTests(TestCase):
    def test_user_registration(self):
        
        
        # Step 1: Prepare data for the POST request (valid form data)
        user_data = {
            'username': 'testuser',
            'password1': 'testing1234',
            'password2': 'testing1234',
        }

        # Step 2: Send a POST request to the registration page with valid data
        response = self.client.post(reverse('register'), user_data)

        # Step 3: Check if the response is a redirect to the index page
        assert response.status_code == 302  # Should redirect after successful form submission
        assert response.url == reverse('index')  # Redirect to the 'index' page

        # Step 4: Check if the user was created in the database
        user = User.objects.get(username='testuser')
        assert user is not None  # The user should exist in the database

        # Step 5: Check if the user is logged in after successful registration
        assert response.wsgi_request.user.is_authenticated  # The user should be authenticated

    @pytest.mark.django_db
    def test_user_registration_invalid_data(self):
        
        
        # Step 1: Prepare invalid data (passwords don't match)
        user_data = {
            'username': 'testuser',
            'password1': 'testing1234',
            'password2': 'password456',  # Passwords don't match
        }

        # Step 2: Send a POST request with invalid data
        response = self.client.post(reverse('register'), user_data)

        # Step 3: Check that the form is re-rendered with errors
        assert response.status_code == 200  # The page should not redirect
        assert 'password2' in response.context['form'].errors  # The password confirmation should fail
    
    def test_user_registration_get(self):
        
        # Make a GET request to the user registration page
        response = self.client.get(reverse('register'))

        # Assert that the response status code is 200 (OK)
        assert response.status_code == 200
        
        # Check if the form is included in the context
        assert 'form' in response.context
        assert isinstance(response.context['form'], UserCreationForm)
