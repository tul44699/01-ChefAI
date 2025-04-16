import io
from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from chef_ai.models import Ingredient  # adjust import to your actual app structure

class ScanImagesViewTest(TestCase):
    @patch('chef_ai.views.Model')  # adjust path if needed
    @patch('chef_ai.views.Ingredient')  # mock the Ingredient model too
    def test_scan_images_returns_matched_ingredients(self, mock_ingredient_model, mock_model_class):
        # Create mocks for concepts
        egg = MagicMock()
        egg.name = "egg"
        egg.value = 0.95

        flour = MagicMock()
        flour.name = "flour"
        flour.value = 0.80

        shoe = MagicMock()
        shoe.name = "shoe"
        shoe.value = 0.10

        mock_prediction = MagicMock()
        mock_prediction.outputs[0].data.concepts = [egg, flour, shoe]
    
        mock_model = MagicMock()
        mock_model.predict_by_bytes.return_value = mock_prediction
        mock_model_class.return_value = mock_model

        # Mock Ingredient DB query
        mock_ingredient_model.objects.values_list.return_value = ['Egg', 'Flour', 'Butter']

        # Simulate image upload
        image_file = SimpleUploadedFile("test.jpg", b"fake-image-data", content_type="image/jpeg")

        response = self.client.post(
            reverse('scan-images'),  # make sure this matches your URLconf
            {'images': [image_file]},
            format='multipart'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        self.assertJSONEqual(
            response.content,
            {"ingredients": ["Egg", "Flour"]}
        )
