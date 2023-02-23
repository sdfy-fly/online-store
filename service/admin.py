from django.contrib import admin

from .models import Item, Order

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id' , 'name' , 'description' , 'price' , 'currency')
    list_display_links  = ('id' , 'name')
    search_fields = ('name' ,)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id' , 'user_id' , 'item')
    search_fields = ('user_id' ,)
