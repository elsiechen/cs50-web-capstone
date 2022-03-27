from django.contrib import admin
from .models import User, Meal, Size, Price, Address, OrderItem, Cart

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username")
class MealAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "type", "image", "price")
class SizeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
class PriceAdmin(admin.ModelAdmin):
    list_display = ("id", "meal", "size", "price")
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "address")
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "meal", "size", "price", "qty", "created_time")
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_time","delivery","delivery_time","address","fee","subtotal","tax","total","utensils","note")


# Register your models here.

admin.site.register(Meal, MealAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Cart, CartAdmin)