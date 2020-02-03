from django.db import models
from django.shortcuts import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


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



class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.quantity} of '{self.item.title}'"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - \
            self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()



class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    province = models.CharField(max_length=50, choices=[])
    city = models.CharField(max_length=50, choices=[])
    street_address = models.CharField(max_length=10)
    zip_code = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}: {self.province}"
    
    class Meta:
        verbose_name_plural = 'Addresses'



class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    card_number = models.CharField(max_length=16)
    transaction_id = models.CharField(max_length=50)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    
    # delivery
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    
    # refund
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)
    ref_code = models.CharField(max_length=24, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total
