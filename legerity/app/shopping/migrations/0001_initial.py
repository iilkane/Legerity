# Generated by Django 5.0.7 on 2025-07-01 12:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('satisfaction_percent', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='carts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='shopping.cart')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.IntegerField()),
                ('address', models.CharField(max_length=255)),
                ('zip_code', models.CharField(max_length=255)),
                ('phone_number', models.IntegerField(db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Prepared', 'Prepared'), ('Delivered', 'Delivered'), ('Canceled', 'Canceled')], db_index=True, default='Prepared', max_length=10, verbose_name='Status')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(db_index=True, decimal_places=2, max_digits=10)),
                ('stock', models.IntegerField(db_index=True)),
                ('sales_number', models.BigIntegerField(db_index=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shopping.category')),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='shopping.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shopping.product')),
            ],
        ),
        migrations.AddIndex(
            model_name='cart',
            index=models.Index(fields=['user'], name='cart_user'),
        ),
        migrations.AddIndex(
            model_name='cartitem',
            index=models.Index(fields=['cart'], name='cart_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['phone_number'], name='phone_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['status'], name='shopping_or_status_55c92b_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['user'], name='user_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['price'], name='price_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['stock'], name='stock_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['category'], name='category_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['sales_number'], name='sales_idx'),
        ),
        migrations.AddIndex(
            model_name='orderproduct',
            index=models.Index(fields=['order'], name='order_idx'),
        ),
    ]
