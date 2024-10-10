# products/serializers.py
from rest_framework import serializers
from .models import Product, Variant

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ['name']

class ProductSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True)

    class Meta:
        model = Product
        fields = ['name', 'variants']

    def create(self, validated_data):
        # Extract variants data from validated data
        variants_data = validated_data.pop('variants', [])
        
        # Create the product instance
        product = Product.objects.create(**validated_data)
        
        # Create each variant and associate it with the product
        for variant_data in variants_data:
            Variant.objects.create(product=product, **variant_data)
        
        return product

    def to_representation(self, instance):
        # Override representation to include variants
        representation = super().to_representation(instance)
        representation['variants'] = VariantSerializer(instance.variants.all(), many=True).data
        return representation