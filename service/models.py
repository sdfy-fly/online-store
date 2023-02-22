from django.db import models
from django.urls import reverse

class Item(models.Model):

    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    img_url = models.CharField(max_length=100, verbose_name='Ссылка на фото')
    price = models.FloatField(verbose_name='Цена')
    currency = models.CharField(max_length=10, verbose_name='Валюта')

    def get_absolute_url(self):
        return reverse('item' , kwargs={"id" : self.id})
    
    def __str__(self) -> str:
        return self.name
