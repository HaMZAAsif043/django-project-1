from rest_framework import serializers
from products_app.models import ProductModel

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = [
            'title',
            'description',
            'price'
        ]