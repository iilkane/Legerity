from django.contrib import admin
from shopping.models import About,Review, Category,Cart,CartItem,Order,OrderProduct,Product
# Register your models here.

# class CategoryAdmin(admin.ModelAdmin):
#     list_display=['id','title']

class ProductAdmin(admin.ModelAdmin):
    list_display=['category','price','stock']

class CartItemAdmin(admin.ModelAdmin):
    list_display=['cart','product','quantity']

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at')


admin.site.register(About)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(Product,ProductAdmin)