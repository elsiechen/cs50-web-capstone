from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Meal(models.Model):
    TYPE_CHOICES = (
        ('APPETIZER', 'Appetizer'),
        ('ENTRE', 'Entre'),
        ('DESSERT', 'Dessert'),
        ('SOUP','Soup'),
        ('DRINK', 'Drink')
    )
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=300, choices = TYPE_CHOICES)
    size = models.ManyToManyField('Size', through='Price', related_name='meals')
    image = models.ImageField(upload_to='images/')
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    def __str__(self):
        return self.name

class Size(models.Model):
    SIZE_CHOICES = (
        ('B', 'Base'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large')
    )
    name = models.CharField(max_length=300, choices = SIZE_CHOICES, default = 'B')

    def __str__(self):
        return self.name

class Price(models.Model):
    meal = models.ForeignKey(Meal, related_name='prices', on_delete=models.CASCADE)
    size = models.ForeignKey(Size, related_name='prices', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return "{}_{}".format(self.meal.__str__(), self.size.__str__())

class Address(models.Model):
    user = models.ForeignKey(User, related_name="address", on_delete=models.CASCADE)
    address = models.CharField(max_length=500)
   
    def __str__(self):
        return f"{self.user} wants food to be delivered at {self.address}"

class OrderItem(models.Model):
    user = models.ForeignKey(User, related_name="orderitems", on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, related_name='orderitems', on_delete=models.CASCADE)
    size = models.ForeignKey(Size, related_name='orderitems', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    qty = models.IntegerField()
    created_time = models.DateTimeField(auto_now_add=True)

    @property
    def amount(self):
        return self.price*self.qty

    def __str__(self):
        return f"{self.user} adds {self.qty} {self.size} of {self.meal} to cart"

class Cart(models.Model):
    user = models.ForeignKey(User, related_name="carts", on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    delivery = models.BooleanField(default="True")
    delivery_time = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    fee = models.DecimalField(max_digits=5, decimal_places=2)
    subtotal = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total =models.DecimalField(max_digits=5, decimal_places=2, default=0)
    utensils = models.BooleanField(default="False")
    orderitems = models.ManyToManyField("OrderItem", related_name="carts", blank=True)
    note = models.TextField()

    def __str__(self):
        return f"{self.user} place an order at {self.created_time}."

