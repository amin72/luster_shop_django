from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import (
    Item,
    OrderItem,
    Order,
    Category,
)
from .mixins import (
    CategoriesMixIn,
)



class ItemListView(CategoriesMixIn, ListView):
    model = Item



class ItemDetailView(CategoriesMixIn, DetailView):
    model = Item



def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False)

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        # check if the order item in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect('product:cart')
        else:
            messages.info(request, "This item was added to your cart.")
            order_item.quantity = 1
            order_item.save()
            order.items.add(order_item)
            return redirect('product:cart')
    else:
        # order does not exist. create order and add order item to it.
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,
            ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect('product:cart')



class CartView(LoginRequiredMixin, View):
    template_name = 'product/cart.html'

    def get(self, request, *args, **kwargs):
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            return render(request, self.template_name, {'object': order})
        except ObjectDoesNotExist:
            messages.error(request, "You do not have an active order")
            return redirect('product:list')
