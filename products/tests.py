from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product, ProductVariant  

class ProductAPITests(APITestCase):

    def setUp(self):
        self.url = reverse('bulk_insert_products')  

    def test_bulk_insert_products(self):
        # Sample data for bulk insertion
        data = [
            {
                "name": "Phone",
                "image": None,  
                "variants": [
                    {
                        "SKU": "PHN-001",
                        "name": "Smartphone",
                        "price": 699.99,
                        "details": "Latest model smartphone"
                    },
                    {
                        "SKU": "PHN-002",
                        "name": "Cellphone",
                        "price": 199.99,
                        "details": "Basic cellphone with calling features"
                    }
                ]
            },
            {
                "name": "Ice Cream",
                "image": None,
                "variants": [
                    {
                        "SKU": "ICE-001",
                        "name": "Chocolate",
                        "price": 2.50,
                        "details": "Rich chocolate flavor"
                    },
                    {
                        "SKU": "ICE-002",
                        "name": "Mint",
                        "price": 2.75,
                        "details": "Refreshing mint flavor"
                    }
                ]
            }
        ]

        # Make the POST request
        response = self.client.post(self.url, data, format='json')

        # Check that the response status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify that the products and variants were created
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(ProductVariant.objects.count(), 4)  

        # Verify the details of the first product
        phone = Product.objects.get(name="Phone")
        self.assertEqual(phone.variants.count(), 2)
        self.assertEqual(phone.variants.first().name, "Smartphone")
        self.assertEqual(phone.variants.first().SKU, "PHN-001")
        self.assertEqual(phone.variants.first().price, 699.99)
        self.assertEqual(phone.variants.first().details, "Latest model smartphone")

    def test_bulk_insert_invalid_data(self):
        # Sample invalid data (missing name for product)
        invalid_data = [
            {
                "variants": [
                    {
                        "SKU": "ICE-001",
                        "name": "Chocolate",
                        "price": 2.50,
                        "details": "Rich chocolate flavor"
                    },
                    {
                        "SKU": "ICE-002",
                        "name": "Mint",
                        "price": 2.75,
                        "details": "Refreshing mint flavor"
                    }
                ]
            }
        ]

        # Make the POST request with invalid data
        response = self.client.post(self.url, invalid_data, format='json')

        # Check that the response status code is 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
