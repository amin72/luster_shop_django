from django.db import models
from django.shortcuts import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    label = models.CharField(max_length=100)
    position = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['position']
        verbose_name_plural = 'Categories'



class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    discount_price = models.PositiveIntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, null=True,
        on_delete=models.SET_NULL)
    slug = models.SlugField(unique=True, allow_unicode=True)
    description = models.TextField()
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('product:detail', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-created_at']
