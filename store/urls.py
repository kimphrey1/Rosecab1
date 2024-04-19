from django.urls import path
from . import views

app_name = "store"
urlpatterns = [
    path("", views.home_view, name="home"), #homepage/ landing page
    # path("pizza/", views.pizzas, name="pizzas"),
    # path("drinks/", views.drinks, name="drinks"),
    # path("sides/", views.sides, name="sides"),
    path("afterlogin/", views.products, name="afterlogin"), #customer dashboard
    path("products/", views.products, name="products"),  #customer dashboard
]
