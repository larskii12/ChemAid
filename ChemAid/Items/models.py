from django.db import models
from datetime import date
from Users.models import User
from datetime import datetime, timedelta
# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    picture = models.FileField()

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category)
    available = models.FloatField(default=0)
    picture = models.ImageField(blank=False, upload_to = 'profile_pics')
    description = models.CharField(max_length=500)

class Pending(models.Model):
    user_borrow = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name_of_item = models.CharField(max_length=255)
    cat_name = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    num_of_items = models.FloatField(default=0)
    picture = models.ImageField(blank=False, upload_to='profile_pics')
    date = models.DateField(default=date.today)
    description = models.CharField(max_length=500)

class Borrow(models.Model):
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name_item = models.CharField(max_length=255)
    cat_name = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    num_of_items = models.FloatField(default=0)
    picture = models.ImageField(blank=False, upload_to='profile_pics')
    date = models.DateField(default=date.today)
    due_date = models.DateField(default=datetime.now()+timedelta(days=7))
    description = models.CharField(max_length=500)

