from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product, Variant

class ProductAPITests(APITestCase):

    def setUp(self):
        self.url = reverse('bulk_insert_products')  

    def test_bulk_insert_products(self):
        # Sample data for bulk insertion
        data = [
            {
                "name": "Phone",
                "variants": [
                    {"name": "Smartphone"},
                    {"name": "Cellphone"}
                ]
            },
            {
                "name": "Ice Cream",
                "variants": [
                    {"name": "Chocolate"},
                    {"name": "Mint"}
                ]
            }
        ]

        # Make the POST request
        response = self.client.post(self.url, data, format='json')

        # Check that the response status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify that the products and variants were created
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Variant.objects.count(), 4)

        # Verify the details of the first product
        Phone = Product.objects.get(name="Phone")
        self.assertEqual(Phone.variants.count(), 2)
        self.assertEqual(Phone.variants.first().name, "Smartphone")

    def test_bulk_insert_invalid_data(self):
        # Sample invalid data (missing name for product)
        invalid_data = [
            {
                "variants": [
                    {"name": "Chocolate"},
                    {"name": "Mint"}
                ]
            }
        ]

        # Make the POST request with invalid data
        response = self.client.post(self.url, invalid_data, format='json')

        # Check that the response status code is 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

