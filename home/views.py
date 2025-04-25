from django.shortcuts import render, redirect
from django.views.generic import ListView
from products.models import Product
from decimal import Decimal, InvalidOperation

# Redirection de la racine vers /home/
def RedirectHomeView(request):
    '''
    Redirige l'URL de '/' vers '/home/'
    '''
    return redirect('home')


class HomeView(ListView):
    template_name = 'home.html'
    model = Product
    context_object_name = 'object_list'

    def get(self, request):
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        queryset = Product.objects.all()

        try:
            if min_price:
                queryset = queryset.filter(price__gte=Decimal(min_price))
            if max_price:
                queryset = queryset.filter(price__lte=Decimal(max_price))
        except (InvalidOperation, ValueError):
            # En cas de filtre invalide, ignorer simplement les filtres
            queryset = Product.objects.none()

        self.object_list = queryset
        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)
