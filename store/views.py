from django.shortcuts import render
from .models import Product, Category
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect,HttpResponse


def products(request):
    products = Product.objects.all()
    # get the keywords from the search field to alter products list
    product_name = request.GET.get("product")
    if product_name != "" and product_name is not None:
        products = products.filter(name__icontains=product_name)
    else:
        # if no item is searched input value is empty
        product_name = ""

    # pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get("page")
    products = paginator.get_page(page_number)

    # search_string is used to display input value as searched product
    context = {"products": products, "search_string": product_name}
    return render(request, "store/products.html", context=context)


def pizzas(request):
    products = Product.objects.filter(product_category__name="Pizza")
    context = {"products": products}
    return render(request, "store/pizzas.html", context=context)


def drinks(request):
    products = Product.objects.filter(product_category__name="Drink")
    context = {"products": products}
    return render(request, "store/drinks.html", context=context)


def sides(request):
    products = Product.objects.filter(product_category__name="Side")
    context = {"products": products}
    return render(request, "store/sides.html", context=context)

#customer afterlogin
def afterlogin(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # get the keywords from the search field to alter products list
    product_name = request.GET.get("product", "")
    category_name = request.GET.get("category", "")

# search function
    if product_name != "" and product_name is not None:
        products = products.filter(name__icontains=product_name)
    else:
        # if no item is searched input value is empty
        product_name = ""

 # filter category
    if category_name:
        selected_category = Category.objects.get(name=category_name)
        products = Product.objects.filter(product_category=selected_category)
        no_products_for_category = not products.exists()
    else:
        products = Product.objects.all()
        no_products_for_category = False

    # pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get("page")
    products = paginator.get_page(page_number)

    # search_string is used to display input value as searched product
    context = {"products": products, "search_string": product_name, 'categories': categories,
        'selected_category': category_name,"no_products_for_category": no_products_for_category,}
    return render(request, 'afterlogin.html',context=context)

def home_view(request):
    products=Product.objects.all()
    if 'product_ids' in request.COOKIES:
        product_ids = request.COOKIES['product_ids']
        counter=product_ids.split('|')
        product_count_in_cart=len(set(counter))
    else:
        product_count_in_cart=0
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect('afterlogin')
    return render(request,'home/index.html',{'products':products,'product_count_in_cart':product_count_in_cart})






