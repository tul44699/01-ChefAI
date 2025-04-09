from django.test import TestCase
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from chef_ai.forms import UserRegistration

class UserRegistrationFormTest(TestCase):

    def test_user_registration_form_valid(self):
        # Valid data
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testing1234',
            'password2': 'testing1234',
        }

        form = UserRegistration(data)
        print(f"Error: {form.errors}")
        self.assertTrue(form.is_valid())  # The form should be valid when all fields are correct

        # Check if the user is created after form validation
        form.save()

        user = User.objects.get(username='testuser')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        

    def test_user_registration_form_invalid_email(self):
        # Invalid email address
        data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password1': 'testing1234',
            'password2': 'testing1234',
        }

        form = UserRegistration(data)
        self.assertFalse(form.is_valid())  # The form should be invalid due to incorrect email
        self.assertIn('email', form.errors)  # There should be an email validation error

    def test_user_registration_form_password_mismatch(self):
        # Passwords don't match
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testing1234',
            'password2': 'differentpassword123',
        }

        form = UserRegistration(data)
        self.assertFalse(form.is_valid())  # The form should be invalid due to password mismatch
        self.assertIn('password2', form.errors)  # There should be a password mismatch error

    def test_user_registration_form_missing_fields(self):
        # Missing required fields
        data = {
            'username': 'testuser',
            'password1': 'testing1234',
            'password2': 'testing1234',
        }

        form = UserRegistration(data)
        self.assertFalse(form.is_valid())  # The form should be invalid due to missing email field
        self.assertIn('email', form.errors)  # There should be an email validation error
