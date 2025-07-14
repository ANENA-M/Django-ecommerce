from django.db import models
from customers.models import Customer
from products.models import products
from decimal import Decimal

# Create your models here.
class order(models.Model):
    LIVE=1
    DELETE=0
    DELETE_CHOICES=((LIVE,'Live'),(DELETE,'Delete'))
    CART_STAGE=1
    ORDER_CONFIRMED=0
    ORDER_PROCESSED=2
    # PROCESSING_STAGE = ORDER_PROCESSED
    ORDER_DELIVERD=3
    ORDER_REJECTED=4
    STATUS_CHOICE=((CART_STAGE,"cart"),
                   (ORDER_CONFIRMED,"confirmed"),
                   (ORDER_PROCESSED,"processed"),
                   (ORDER_DELIVERD,"deliverd"),
                   (ORDER_REJECTED,"rejected")
                   )
    
    order_status=models.IntegerField(choices=STATUS_CHOICE,default=CART_STAGE)
   
    owner=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,related_name='orders')
    delete_status=models.IntegerField(choices=DELETE_CHOICES,default=LIVE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def update_total(self):
        subtotal = Decimal('0.00')
        for item in self.added_items.all():
            if item.product and item.product.price:
                subtotal += Decimal(item.product.price) * item.quantity
        tax = subtotal * Decimal('0.05')
        self.total = subtotal + tax
        self.save()
   
    def __str__(self) -> str:
        if self.owner:
            return f"order-{self.id}-{self.owner.user.username}"
        return f"order-{self.id}-no-owner"
        # return "order-{}-{}".format(self.id,self.owner.user.username)
    

class orderdItem(models.Model):
    product=models.ForeignKey(products,related_name='added_carts',on_delete=models.SET_NULL,null=True)
    quantity=models.IntegerField(default=1)
    owner=models.ForeignKey(order,on_delete=models.CASCADE,related_name='added_items')
    
