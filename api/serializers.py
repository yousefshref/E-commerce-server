from rest_framework import serializers
from . import models


"""
Auth
"""
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.User





"""
Category
"""
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Category


"""
State
"""
class StateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.State

"""
Brand
"""
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Brand
"""
Color
"""
class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Color




"""
Product
"""
class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.ProductImage

class VariantSerializer(serializers.ModelSerializer):
    color_details = ColorSerializer(read_only=True, source='color')
    class Meta:
        fields = '__all__'
        model = models.Variant

class RelatedProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    class Meta:
        fields = '__all__'
        model = models.Product

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    variants = VariantSerializer(many=True, source='product_variant')
    related = RelatedProductSerializer(many=True)
    brand_details = BrandSerializer(read_only=True, source='brand')
    category_details = CategorySerializer(read_only=True, source='category')
    class Meta:
        fields = '__all__'
        model = models.Product



"""
Cart
"""
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Cart



class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    cart = CartSerializer(read_only=True)
    class Meta:
        fields = '__all__'
        model = models.CartItem


"""
Order
"""
class OrderItemSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)
    class Meta:
        fields = '__all__'
        model = models.OrderItem


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    state_details = StateSerializer(read_only=True, source='state')

    class Meta:
        fields = '__all__'
        model = models.Order

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items', None)
        order = models.Order.objects.create(**validated_data)

        if order_items_data:
            for order_item_data in order_items_data:
                models.OrderItem.objects.create(order=order, **order_item_data)

        return order



class LandingSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = models.Landing

class SettingsSerializer(serializers.ModelSerializer):
    category_1 = CategorySerializer()
    category_2 = CategorySerializer()
    category_3 = CategorySerializer()
    new = ProductSerializer(many=True)
    popular = ProductSerializer(many=True)
    landing = LandingSerializer(source='setting_landing', many=True)
    class Meta:
        fields = '__all__'
        model = models.Settings