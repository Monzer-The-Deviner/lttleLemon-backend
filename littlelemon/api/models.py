from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from django.conf import settings
class Reservation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="resurvations")
    party_size = models.IntegerField()
    time = models.DateTimeField()
    notes = models.TextField(blank=True,null=True)

class Category(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=255,db_index=True)
    image = models.ImageField(upload_to='images/',default='images/default.jpg')
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs) 
    def __str__(self):
        return self.title


class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ManyToManyField(Category,related_name="items")
    image = models.ImageField(upload_to="images/",default='images/default.jpg')
    description = models.TextField( default='')
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem,on_delete= models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(MenuItem)
    status = models.IntegerField(choices=((0, 'In Progress'), (1, 'Delivered')),default=0)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL,related_name="delivery_crew", null=True)
    date = models.DateField(db_index=True,auto_now_add=True)
    address = models.TextField(default='')
    phone_number = models.CharField(max_length=15,blank=True,null=True,default='')
    total_price = models.DecimalField(max_digits=6,decimal_places=2,default=0)
    def __str__(self):
        return f'{self.user} has orderd'
    
class OrderItem (models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_items')
    menu_item = models.ForeignKey(MenuItem,on_delete= models.CASCADE)
    quantity = models.SmallIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    