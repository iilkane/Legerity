from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient,APITestCase
from rest_framework import status
from .models import Product, Category,Cart, CartItem,Order,OrderProduct,User
from shopping.api.serializers import ProductListSerializer,CartItemCreateSerializer,CartItemUpdateSerializer,CartListSerializer
from rest_framework.authtoken.models import Token

# Create your tests here.

class ProductListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.category = Category.objects.create(title="shoes")
        self.product = Product.objects.create(
            category=self.category,
            info="<p>new shoes</p>",
            price=100.99,
            stock=5,
            sales_number=1,
        )
        self.url = reverse('products')

    def test_product_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = ProductListSerializer([self.product], many=True).data
        self.assertEqual(response.data, expected_data)

    def test_product_list_fields(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product = response.data[0]

        expected_fields = ['id', 'name', 'info', 'price', 'image', 'category']
        for field in expected_fields:
            self.assertIn(field, product)


class CartItemViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(email='lily@lay.com', password='lily123')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.category = Category.objects.create(title='shoes')
        self.product = Product.objects.create(
            category=self.category,
            info="<p>shoes</p>",
            price=100.99,
            stock=5,
            sales_number=1,
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            product=self.product,
            cart=self.cart,
            quantity=2
        )
        self.new_product = Product.objects.create(
            category=self.category,
            info="<p>shoes</p>",
            price=50.50,
            stock=10,
            sales_number=0,
        )

        self.list_url = reverse('cart-item-list')
        self.detail_url = lambda pk: reverse('cart-item-detail', kwargs={'pk': pk})

    def test_cart_items_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = CartListSerializer(self.cart).data
        self.assertEqual(response.data, expected_data)

    def test_create_cart_item(self):
        data = {
            'product': self.new_product.id,
            'quantity': 3
        }

        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        cart_item = CartItem.objects.get(cart=self.cart, product=self.new_product)
        expected_data = CartItemCreateSerializer(cart_item).data
        self.assertEqual(response.data, expected_data)

    def test_not_enough_stock(self):
        data = {
            'product': self.new_product.id,
            'quantity': 15
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Not enough stock', str(response.data))

    def test_partial_update_quantity(self):
        url = self.detail_url(self.cart_item.id)
        data = {'quantity': 5}

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.cart_item.refresh_from_db()

        expected_data = CartItemUpdateSerializer(self.cart_item).data
        self.assertEqual(response.data, expected_data)

    def test_partial_update_quantity_not_enough_stock(self):
        url = self.detail_url(self.cart_item.id)
        data = {'quantity': 15}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Not enough stock', str(response.data))

    def test_delete_cart_item(self):
        url = self.detail_url(self.cart_item.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CartItem.objects.filter(id=self.cart_item.id).exists())


class OrderViewTest(APITestCase):
    def setUp(self):
        self.client= APIClient()
        self.user=User.objects.create_user(email='lily@lay.com', password='lily123')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.category=Category.objects.create(title='shoes')
        self.product=Product.objects.create( 
            category=self.category,
            info="<p>shoes</p>",
            price=200,
            stock=20,
            sales_number=2
        )
        self.cart=Cart.objects.create(user=self.user)
        self.cart_item=CartItem.objects.create(
            product=self.product,
            cart=self.cart,
            quantity=5
        )

        self.url=reverse('checkout')

    def test_order_create(self):
        data = {
            'address': '123 Street',
            'zip_code': '122ab',
            'phone_number': '+994552224477'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        order = Order.objects.filter(user=self.user).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.total_price, self.product.price * self.cart_item.quantity)

        self.assertFalse(CartItem.objects.filter(cart=self.cart).exists())

        order_product = OrderProduct.objects.filter(order=order, product=self.product).first()
        self.assertIsNotNone(order_product)
        self.assertEqual(order_product.quantity, self.cart_item.quantity)
        





