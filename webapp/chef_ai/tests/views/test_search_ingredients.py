import pytest
from django.urls import reverse
from django.test import Client
from chef_ai.models import Ingredient

@pytest.mark.django_db
def test_search_ingredients():
    # Step 1: Create test ingredients in the database
    Ingredient.objects.create(ingredient_name='Tomato')
    Ingredient.objects.create(ingredient_name='Tortilla')
    Ingredient.objects.create(ingredient_name='Lettuce')
    
    # Step 2: Create a client instance for sending requests
    client = Client()

    # Step 3: Send a GET request with a query
    response = client.get(reverse('search_ingredients'), {'q': 'to'})  # searching for ingredients starting with 'to'
    
    # Step 4: Check that the response is a JsonResponse
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/json'

    # Step 5: Parse the JSON response and check if the correct results are returned
    data = response.json()
    assert 'results' in data
    assert data['results'] == ['Tomato', 'Tortilla']  # The ingredients that start with 'to'

@pytest.mark.django_db
def test_search_ingredients_no_match():
    # Step 1: Create test ingredients in the database
    Ingredient.objects.create(ingredient_name='Tomato')
    Ingredient.objects.create(ingredient_name='Lettuce')

    # Step 2: Create a client instance for sending requests
    client = Client()

    # Step 3: Send a GET request with a query that doesn't match any ingredient
    response = client.get(reverse('search_ingredients'), {'q': 'carrot'})  # searching for an ingredient 'carrot' which does not exist

    # Step 4: Check that the response is a JsonResponse
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/json'

    # Step 5: Parse the JSON response and check if an empty list is returned
    data = response.json()
    assert 'results' in data
    assert data['results'] == []  # No ingredients starting with 'carrot'

@pytest.mark.django_db
def test_search_ingredients_empty_query():
    # Step 1: Create test ingredients in the database
    Ingredient.objects.create(ingredient_name='Tomato')
    Ingredient.objects.create(ingredient_name='Tuna')
    Ingredient.objects.create(ingredient_name='Lettuce')

    # Step 2: Create a client instance for sending requests
    client = Client()

    # Step 3: Send a GET request with an empty query
    response = client.get(reverse('search_ingredients'), {'q': ''})  # empty query

    # Step 4: Check that the response is a JsonResponse
    assert response.status_code == 200
    assert response['Content-Type'] == 'application/json'

    # Step 5: Parse the JSON response and check if the correct results are returned
    data = response.json()
    assert 'results' in data
    assert data['results'] == []  # Expecting an empty list for results when query is empty
