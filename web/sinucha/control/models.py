from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

class User_Data(models.Model):

    USER = 'user'
    ADMIN = 'admin'
    
    ROL_CHOICES = (
        (USER, 'USER'),
        (ADMIN, 'ADMIN'),
    )
    
    tagRfid = models.CharField(max_length=64, blank=False)
    chatid = models.DecimalField(max_digits=12, decimal_places=0)
    balance_actual = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    username = models.CharField(max_length=20, blank=False)
    user = models.ForeignKey(User)
    rol = models.CharField(max_length=5,
                                      choices=ROL_CHOICES,
                                      default=USER,
                                      blank=False,
                                      )
                                      
    def __str__(self):
        return '{}'.format(self.username)


class Balance(models.Model):

    CASH = 'cash'
    PAYPAL = 'PayPal'
    
    TYPE_PAYMENT = (
        (CASH, 'CASH'),
        (PAYPAL, 'PAYPAL'),
    )
    
    user = models.ForeignKey(User_Data, blank=False)
    amount_entered = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=False)
    type_amount = models.CharField(max_length=5,
                                      choices=TYPE_PAYMENT,
                                      default=CASH,
                                      blank=False,
                                      )
    date = models.DateTimeField( default=datetime.datetime.now() )
    
    def __str__(self):
        return '{}: +{}'.format(self.user, self.amount_entered)


class Item(models.Model):

    name = models.CharField(max_length=30, blank=False)
    barcode = models.CharField(max_length=30, blank=False)
    price_sale = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    stock = models.IntegerField(blank=False, default=0)
    
    def __str__(self):
        return '{}'.format(self.name)
    
    
class Shopping_History(models.Model):
    
    MERCADONA = 'mercadona'
    LIDL = 'lidl'
    OTRO =  'otro'
    
    TYPE_SUPERMARKET = (
        (MERCADONA, 'MERCADONA'),
        (LIDL, 'LIDL'),
        (OTRO, 'OTRO'),
    )
    
    item = models.ForeignKey(Item, blank=False)
    date = models.DateTimeField( default=datetime.datetime.now() )
    units = models.IntegerField(default=0)
    unit_purchase_price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    supermarket = models.CharField(max_length=9,
                                      choices=TYPE_SUPERMARKET,
                                      default=OTRO,
                                      blank=False,
                                      )
    
    def __str__(self):
        return '{} - {}'.format(self.item, self.date)
    
    
class Sale_History(models.Model):

    item = models.ForeignKey(Item, blank=False)
    user = models.ForeignKey(User_Data, blank=False)
    date = models.DateTimeField( default=datetime.datetime.now() )
    price_sale = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    price_cost = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    def __str__(self):
        return '{} - {}'.format(self.item, self.user)
 
        
@receiver(post_save, sender=Shopping_History, dispatch_uid="create_stock_item")
def create_stock(sender, instance, **kwargs):
    object_product = Item.objects.get(id=instance.item.id)
    object_product.stock += instance.units
    object_product.save()

#import pdb; pdb.set_trace()