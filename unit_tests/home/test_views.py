from django.urls import reverse 
from django.test import Client
from pytest_django.asserts import assertTemplateUsed
import pytest

from products.models import Product


@pytest.mark.django_db
def test_HomeView_no_filter():
    """
    Teste la vue Home sans aucun filtre sur les prix.
    Tous les produits doivent être retournés.
    """
    # Création des produits pour le test
    Product.objects.create(name="Product 1", price=10.00)
    Product.objects.create(name="Product 2", price=20.00)
    Product.objects.create(name="Product 3", price=30.00)
    Product.objects.create(name="Product 4", price=40.00)

    client = Client()
    response = client.get(reverse('home'))

    # Teste que la vue renvoie un code de statut 200 (OK)
    assert response.status_code == 200
    assertTemplateUsed(response, 'home.html')

    # Vérifie que tous les produits sont retournés
    assert len(response.context['object_list']) == 4


@pytest.mark.django_db
def test_HomeView_min_price_filter():
    """
    Teste la vue Home avec un filtre sur le prix minimum. 
    Seuls les produits dont le prix est >= min_price doivent être retournés.
    """
    # Création des produits pour le test
    Product.objects.create(name="Product 1", price=10.00)
    Product.objects.create(name="Product 2", price=20.00)
    Product.objects.create(name="Product 3", price=30.00)
    Product.objects.create(name="Product 4", price=40.00)

    client = Client()
    # Envoie une requête avec un filtre min_price
    response = client.get(reverse('home'), {'min_price': 20.00})

    # Teste que la vue renvoie un code de statut 200 (OK)
    assert response.status_code == 200
    assertTemplateUsed(response, 'home.html')

    # Vérifie que seuls les produits avec un prix >= 20 sont retournés
    assert len(response.context['object_list']) == 3


@pytest.mark.django_db
def test_HomeView_max_price_filter():
    """
    Teste la vue Home avec un filtre sur le prix maximum. 
    Seuls les produits dont le prix est <= max_price doivent être retournés.
    """
    # Création des produits pour le test
    Product.objects.create(name="Product 1", price=10.00)
    Product.objects.create(name="Product 2", price=20.00)
    Product.objects.create(name="Product 3", price=30.00)
    Product.objects.create(name="Product 4", price=40.00)

    client = Client()
    # Envoie une requête avec un filtre max_price
    response = client.get(reverse('home'), {'max_price': 30.00})

    # Teste que la vue renvoie un code de statut 200 (OK)
    assert response.status_code == 200
    assertTemplateUsed(response, 'home.html')

    # Vérifie que seuls les produits avec un prix <= 30 sont retournés
    assert len(response.context['object_list']) == 3


@pytest.mark.django_db
def test_HomeView_min_and_max_price_filter():
    """
    Teste la vue Home avec des filtres sur le prix minimum et maximum. 
    Seuls les produits dans l'intervalle [min_price, max_price] doivent être retournés.
    """
    # Création des produits pour le test
    Product.objects.create(name="Product 1", price=10.00)
    Product.objects.create(name="Product 2", price=20.00)
    Product.objects.create(name="Product 3", price=30.00)
    Product.objects.create(name="Product 4", price=40.00)

    client = Client()
    # Envoie une requête avec des filtres min_price et max_price
    response = client.get(reverse('home'), {'min_price': 20.00, 'max_price': 30.00})

    # Teste que la vue renvoie un code de statut 200 (OK)
    assert response.status_code == 200
    assertTemplateUsed(response, 'home.html')

    # Vérifie que seuls les produits avec un prix entre 20 et 30 sont retournés
    assert len(response.context['object_list']) == 2


@pytest.mark.django_db
def test_HomeView_invalid_price_filter():
    """
    Teste la vue Home avec des filtres de prix invalides. Aucun produit ne doit être retourné.
    """
    # Création des produits pour le test
    Product.objects.create(name="Product 1", price=10.00)
    Product.objects.create(name="Product 2", price=20.00)
    Product.objects.create(name="Product 3", price=30.00)
    Product.objects.create(name="Product 4", price=40.00)

    client = Client()
    # Envoie une requête avec des filtres invalides
    response = client.get(reverse('home'), {'min_price': 'invalid', 'max_price': 'invalid'})

    # Teste que la vue renvoie un code de statut 200 (OK)
    assert response.status_code == 200
    assertTemplateUsed(response, 'home.html')

    # Vérifie que tous les produits sont retournés si les filtres sont invalides
    assert len(response.context['object_list']) == 4
