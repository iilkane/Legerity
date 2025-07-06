from django.db import models
from customer.models import User
from tinymce.models import HTMLField

# Create your models here. 

class About(models.Model):
    number_of_personals=models.BigIntegerField(default=0)
    satisfaction_percent=models.IntegerField()
    updated_at = models.DateTimeField('Updated At',auto_now=True)



class Review(models.Model):
    fullname = models.CharField(max_length=255, null=True)
    image = models.CharField(max_length=255, null=True)
    comment = HTMLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname



class Category(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title= models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products', db_index=True)
    info=HTMLField(null=True)
    price=models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    stock=models.IntegerField(db_index=True)
    sales_number=models.BigIntegerField(db_index=True,default=0)
    image = models.ImageField('Product Image', upload_to='products',null=True,blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['price'],name='price_idx'),
            models.Index(fields=['stock'],name='stock_idx'),
            models.Index(fields=['category'],name='category_idx'),
            models.Index(fields=['sales_number'],name='sales_idx'),
        ]
   

class Cart(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='carts', db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['user'], name='cart_user'),
        ]

    def __str__(self):
        return self.user.email

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name="cart_items", db_index=True)
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    quantity=models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['cart'],name='cart_idx'),
        ]

    @property
    def subtotal_price(self):
        return self.product.price * self.quantity


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        prepared = 'Prepared', 'Prepared'
        delivered = 'Delivered', 'Delivered'
        canceled = 'Canceled', 'Canceled'

    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', db_index=True)
    total_price=models.BigIntegerField()
    address=models.CharField(max_length=255)
    zip_code=models.CharField(max_length=255)
    phone_number=models.BigIntegerField( db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField('Status',max_length=10, choices=OrderStatus.choices, default=OrderStatus.prepared, db_index=True)    

    class Meta:
        indexes = [
            models.Index(fields=['phone_number'],name='phone_idx'),
            models.Index(fields=['status']),
            models.Index(fields=['user'],name='user_idx'),
        ]


class OrderProduct(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products', db_index=True)
    product=models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity=models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['order'],name='order_idx'),
        ]


