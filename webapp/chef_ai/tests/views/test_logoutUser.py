from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

class LogoutUserTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testing1234')

    def test_logout_user(self):
        # Log the user in
        self.client.login(username='testuser', password='testing1234')

        # Send a POST request to the logout view and follow the redirect
        response = self.client.post(reverse('logout'), follow=True)  # follow=True ensures that the redirect is followed

        # Ensure the response is a redirect (status code 302)
        self.assertEqual(response.status_code, 200)  # After follow=True, we should get a 200 response at the final destination

        # Ensure the user is redirected to the index page (check the template used)
        self.assertTemplateUsed(response, 'index.html')

        # Ensure the user is logged out (should be an instance of AnonymousUser)
        user = response.context['user']
        self.assertTrue(user.is_anonymous)  # After logout, the user should be anonymous


