from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product

# Redirection de la racine vers /home/
def RedirectHomeView(request):
    '''
    Redirige l'URL de '/' vers '/home/'
    '''
    return redirect('home')

class HomeView(ListView):
    '''
    Renders la page d'accueil avec tous les produits
    '''
    template_name = 'home.html'
    model = Product
    context_object_name = 'object_list'  # Cette variable sera utilisée dans le template pour les produits

    def get(self, request, *args, **kwargs):
        # Récupérer les paramètres de prix dans la requête GET
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        # Récupérer les produits sans filtrer au départ
        queryset = Product.objects.all()

        # Appliquer les filtres si les paramètres sont fournis
        if min_price:
            queryset = queryset.filter(price__gte=min_price)  # Filtrer les produits dont le prix est >= min_price
        if max_price:
            queryset = queryset.filter(price__lte=max_price)  # Filtrer les produits dont le prix est <= max_price

        # Affecter la liste filtrée ou non filtrée à l'objet 'object_list'
        self.object_list = queryset

        # Rendre la page avec les produits filtrés ou non
        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)
