from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from shopping.models import Review, Product, Cart, CartItem, Category
from shopping.api.serializers import ReviewListSerializer, CategoryListSerializer, ProductListSerializer, CartItemCreateSerializer, CartItemUpdateSerializer, CartListSerializer, OrderCreateSerializer


class ReviewListView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class CartItemViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_cart(self, request):
        ''' Retrieve or create the cart for the authenticated user. '''
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart

    def list(self, request):
        ''' Retrieve all products  in the user's cart. '''
        cart = self.get_cart(request)
        serializer = CartListSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        cart = self.get_cart(request)
        product_id = request.data.get('product')
        quantity = request.data.get('quantity')
    
        if not product_id:
            return Response({'product': 'This field is required'}, status=status.HTTP_400_BAD_REQUEST)
    
        if not quantity:
            return Response({'quantity': 'This field is required'}, status=status.HTTP_400_BAD_REQUEST)
    
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    
        if CartItem.objects.filter(cart=cart, product=product).exists():
            return Response({'error': 'Product already in cart. Use PATCH to update quantity'}, status=status.HTTP_400_BAD_REQUEST)
    
        if int(quantity) > product.stock:
            return Response({'error': 'Not enough stock'}, status=status.HTTP_400_BAD_REQUEST)
    
        cart_item = CartItem.objects.create(
            cart=cart, product=product, quantity=quantity)
        serializer = CartItemCreateSerializer(cart_item)
    
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        ''' Update the quantity of an existing cart item (PATCH request). '''
        try:
            cart_item = CartItem.objects.get(id=pk, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

        new_quantity = request.data.get('quantity')
        if new_quantity is None:
            return Response({'error': 'Quantity is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            new_quantity = int(new_quantity)
        except ValueError:
            return Response({'error': 'Quantity must be an integer'}, status=status.HTTP_400_BAD_REQUEST)

        if new_quantity > cart_item.product.stock:
            return Response({'error': 'Not enough stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_item.quantity = new_quantity
        cart_item.save()
        serializer = CartItemUpdateSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        ''' Remove an item from the cart (DELETE request). '''
        try:
            cart_item = CartItem.objects.get(id=pk, cart__user=request.user)
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)


class OrderView(GenericAPIView):
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save() 
        return Response({'message': 'Order placed successfully.'}, status=status.HTTP_201_CREATED)
