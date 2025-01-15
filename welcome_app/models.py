
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
class Profile(models.Model): # the class of a users profile showing all the attributes associated with them
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=100, blank=True)
    surname = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    postcode = models.CharField(max_length=20, blank=True)
    security_question = models.CharField(max_length=255, blank=True)
    security_answer = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username


class Order(models.Model): # the orders class
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_delivery_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs): # calculates the orders delivery date and time placed to add to the order summary
        if not self.estimated_delivery_date:
            self.estimated_delivery_date = datetime.now().date() + timedelta(days=3)
        super().save(*args, **kwargs)

class Product(models.Model): # the class for products again showing the attributes associated with them
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    inventory = models.PositiveIntegerField(default=0)  # New field for inventory

    def __str__(self):
        return self.name

class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='basket')

    def __str__(self):
        return f"{self.user.username}'s Basket"

class BasketItem(models.Model): # the basket items are associated to a specific basket, when the basket s deleted so are the items from the basket as a result of CASCADE
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.basket.user.username}'s Basket"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField() # stores how many of an item is stored in an order

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"