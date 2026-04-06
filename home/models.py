#PROJECT BY INDRASISH BISWAS
from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models import Sum

class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        #now django will not create a table for this model, it will be used as a base class for other models to inherit from


class PizzaCategory(BaseModel):                 #inheritance of BaseModel
    category_name = models.CharField(max_length=100)

class Pizza(BaseModel):                               #inheritance of BaseModel
    category = models.ForeignKey(PizzaCategory, on_delete=models.CASCADE, related_name='pizzas')
    pizza_name = models.CharField(max_length=100)
    price = models.IntegerField(default=100)
    images = models.ImageField(upload_to='pizzas')
    

class Cart(BaseModel):                                #inheritance of BaseModel
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='carts')
    is_paid = models.BooleanField(default=False)
    instamojo_id = models.CharField(max_length=100)

    def get_cart_total(self):
        return CartItem.objects.filter(cart = self).aggregate(Sum('pizza__price'))['pizza__price__sum']

class CartItem(BaseModel):                            #inheritance of BaseModel
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    
