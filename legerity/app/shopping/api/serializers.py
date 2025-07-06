from rest_framework import serializers
from django.core.validators import RegexValidator
from shopping.models import About, Product, Review, Category, CartItem, Cart, Order, OrderProduct
from customer.models import User

phone_number_validator = RegexValidator(
    regex=r'^(\+[0-9]{1,3})?[0-9]{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)


class ReviewListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['fullname', 'image', 'comment']


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'title']


class ProductListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer(read_only=True)
    name = serializers.SerializerMethodField()
    info = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'info', 'price', 'image', 'category']

    def get_name(self, obj):
        return f'{obj.category.title}'

    def get_info(self, obj):
        return str(obj.info) if obj.info else ''


class CartItemListSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    subtotal_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'subtotal_price']

    def get_subtotal_price(self, obj):
        return obj.subtotal_price


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']

    def validate(self, data):
        product = data.get('product')
        quantity = data.get('quantity')
        if product and quantity > product.stock:
            raise serializers.ValidationError('Not enough stock')
        return data


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError('Quantity must be at least 1.')
        return value


class CartListSerializer(serializers.ModelSerializer):
    cart_items = CartItemListSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['cart_items', 'total_price']

    def get_total_price(self, obj):
        total_price = sum(item.product.price *
                          item.quantity for item in obj.cart_items.all())
        return total_price


# class OrderProductSerializer(serializers.ModelSerializer):
#     product=ProductListSerializer(read_only=True)
#     class Meta:
#         model=OrderProduct
#         fields=['product','quantity']


class OrderCreateSerializer(serializers.Serializer):
    address = serializers.CharField()
    zip_code = serializers.CharField()
    phone_number = serializers.CharField(validators=[phone_number_validator])

    def validate(self, attrs):
        user = self.context['request'].user
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            raise serializers.ValidationError("Your cart is empty.")
        if not cart.cart_items.exists():
            raise serializers.ValidationError("Your cart is empty.")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        cart = Cart.objects.get(user=user)

        address = validated_data['address']
        zip_code = validated_data['zip_code']
        phone_number = validated_data['phone_number']

        total_price = sum([
            item.product.price * item.quantity
            for item in cart.cart_items.all()
        ])

        order = Order.objects.create(
            user=user,
            total_price=total_price,
            address=address,
            zip_code=zip_code,
            phone_number=phone_number,
        )

        for item in cart.cart_items.all():
            OrderProduct.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
            )
            item.product.sales_number += item.quantity
            item.product.save()

        cart.cart_items.all().delete()

        return order
