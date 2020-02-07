from .models import Category


class CategoriesMixIn:
    """A mixin to send categories with context"""

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            categories = Category.objects.all()
            context["categories"] = categories
            return context