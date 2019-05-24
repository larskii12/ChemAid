from django.contrib import admin
from .models import Item, Category, Pending, Borrow
# Register your models here.


admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Pending)
admin.site.register(Borrow)