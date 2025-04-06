from django.test import TestCase
from django.urls import reverse
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

    def test_index_data_saved_in_session(self):
        data = {'final_ingredients':'Rice {1 cup}'}

        response = self.client.post(reverse('index'), data)

        session = self.client.session

        self.assertIn('selected_options', session)
        self.assertIn('ai_response', session)
