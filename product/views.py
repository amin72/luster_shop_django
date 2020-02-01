from django.shortcuts import render
from django.views.generic import ListView, DetailView, View

from .models import (
    Item,
)


class ItemListView(ListView):
    model = Item



class ItemDetailView(DetailView):
    model = Item
