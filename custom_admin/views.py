from django.shortcuts import render
from store.models import Category
from store.models import Product,Size, ProductVariant
from django.contrib import messages
from .forms import ProductVariantForm, UserEditForm
from django.urls import reverse
from .forms import ProductForm, ProductVariantFormSet, OrderEditForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from order.models import Order
from users.models import Customer, User
# from .forms import SizeForm
from django.contrib.auth.decorators import login_required

# def adminLogin(request):
#     msg = None
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#         try:
#             if user.is_staff:
#                 login(request, user)
#                 msg = "User login successfully"
#                 return redirect('admindashboard')
#             else:
#                 msg = "Invalid Credentials"
#         except:
#             msg = "Invalid Credentials"
#     dic = {'msg': msg}
#     return render(request, 'admin_login.html', dic)


# Adding driver to admin login

def adminLogin(request):
    msg = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            if user.is_staff:
                login(request, user)
                msg = "User login successfully"
                # Check if the user belongs to the Driver group
                if user.groups.filter(name='Driver').exists():
                    return redirect('driver_view_orders')  # Redirect to driver_view_orders
                else:
                    return redirect('admindashboard')  # Default admin dashboard URL
            else:
                msg = "Invalid Credentials"
        except:
            msg = "Invalid Credentials"
    dic = {'msg': msg}
    return render(request, 'admin_login.html', dic)





























# --------------------------------------------------------------------------------------------------------
def adminHome(request):
    return render(request, 'admin_base.html')

# --------------------------------------------------------------------------------------------------------

def admin_dashboard(request):
    categorycount = Category.objects.all().count()
    productcount = Product.objects.all().count()
    ordercount = Order.objects.all().count()

    # Get the count of all users (including those without accounts)
    all_users_count = User.objects.all().count()

    mydict = {
        'categorycount': categorycount,
        'customercount': all_users_count,
        'productcount': productcount,
        'ordercount': ordercount,
    }
    return render(request, 'admin_dashboard.html', {'mydict': mydict})


# --------------------------------------------------------------------------------------------------------

def add_category(request):
    if request.method == "POST":
        name = request.POST['name']
        Category.objects.create(name=name)
        messages.success(request, "Category added")
        return redirect('view_category')
    return render(request, 'add_category.html', locals())
# --------------------------------------------------------------------------------------------------------


def view_category(request):
    category = Category.objects.all()
    return render(request, 'view_category.html', locals())

# --------------------------------------------------------------------------------------------------------


def edit_category(request, pid):
    category = Category.objects.get(id=pid)
    if request.method == "POST":
        name = request.POST['name']
        category.name = name
        category.save()
        msg = "Category Updated"
    return render(request, 'edit_category.html', locals())

# --------------------------------------------------------------------------------------------------------

def delete_category(request, pid):
    category = Category.objects.get(id=pid)
    category.delete()
    return redirect('view_category')

# --------------------------------------------------------------------------------------------------------

def add_product(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES)
        variant_formset = ProductVariantFormSet(request.POST, prefix='variants')

        if product_form.is_valid() and variant_formset.is_valid():
            product = product_form.save()
            instances = variant_formset.save(commit=False)

            for instance in instances:
                instance.product = product
                instance.save()

            return redirect('view_product')

    else:
        product_form = ProductForm()
        variant_formset = ProductVariantFormSet(prefix='variants')

    return render(request, 'add_product.html', {'product_form': product_form, 'variant_formset': variant_formset})

# --------------------------------------------------------------------------------------------------------


def view_product(request):
    product = Product.objects.all()
    return render(request, 'view_product.html', locals())

# --------------------------------------------------------------------------------------------------------


def edit_product(request, pid):
    product = get_object_or_404(Product, id=pid)
    category = Category.objects.all()

    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        variant_formset = ProductVariantFormSet(request.POST, instance=product, prefix='variants')

        if product_form.is_valid() and variant_formset.is_valid():
            product = product_form.save()
            variant_formset.save()

            messages.success(request, "Product Updated")
            return redirect('view_product')

    else:
        product_form = ProductForm(instance=product)
        variant_formset = ProductVariantFormSet(instance=product, prefix='variants')

    return render(request, 'edit_product.html', {'product_form': product_form, 'variant_formset': variant_formset})

# --------------------------------------------------------------------------------------------------------


def delete_product(request, pid):
    product = Product.objects.get(id=pid)
    product.delete()
    messages.success(request, "Product Deleted")
    return redirect('view_product')

# --------------------------------------------------------------------------------------------------------

def add_size(request):
    if request.method == "POST":
        name = request.POST['name']
        Size.objects.create(name=name)
        msg = "Size added"
    return render(request, 'add_size.html', locals())

# --------------------------------------------------------------------------------------------------------


def view_size(request):
    size = Size.objects.all()
    return render(request, 'view_size.html', locals())

# --------------------------------------------------------------------------------------------------------

def edit_size(request, pid):
    size = Size.objects.get(id=pid)
    if request.method == "POST":
        name = request.POST['name']
        size.name = name
        size.save()
        msg = "Size Updated"
    return render(request, 'edit_size.html', locals())

# --------------------------------------------------------------------------------------------------------

def delete_size(request, pid):
    size = Size.objects.get(id=pid)
    size.delete()
    return redirect('view_size')


# --------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------


def add_productvariant(request, product_id):
    product = Product.objects.get(id=product_id)
    sizes = Size.objects.all()

    if request.method == "POST":
        form = ProductVariantForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            size = form.cleaned_data['size']
            price = form.cleaned_data['price']

            ProductVariant.objects.create(title=title, product=product, size=size, price=price)

            # Add a success message
            messages.success(request, 'Product variant added successfully.')

            # Redirect back to the same page
            return redirect(reverse('add_productvariant', kwargs={'product_id': str(product_id)}))

    else:
        form = ProductVariantForm()

    return render(request, 'add_productvariant.html', {'product': product, 'sizes': sizes, 'form': form})

# --------------------------------------------------------------------------------------------------------


def view_product_variants(request):
    variants = ProductVariant.objects.all()
    return render(request, 'view_product_variants.html', {'variants': variants})

# --------------------------------------------------------------------------------------------------------


def edit_productvariant(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)

    if request.method == "POST":
        form = ProductVariantForm(request.POST, instance=variant)
        if form.is_valid():
            form.save()
            messages.success(request, "Product Variant updated successfully.")
            return redirect('view_product_variants')
    else:
        form = ProductVariantForm(instance=variant)

    return render(request, 'edit_productvariant.html', {'form': form, 'variant': variant})

# --------------------------------------------------------------------------------------------------------


def delete_productvariant(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)

    if request.method == 'POST':
        variant.delete()
        # Add a success message if needed
        return redirect('view_productvariants')  # Redirect to the product variants list view

    return render(request, 'delete_productvariant.html', {'variant': variant})





# --------------------------------------------------------------------------------------------------------

def view_orders(request):
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'view_order.html', context)

# --------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------


def edit_order(request, transaction_id):
    order = get_object_or_404(Order, transaction_id=transaction_id)

    if request.method == 'POST':
        form = OrderEditForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            # Add a success message
            messages.success(request, 'Order successfully edited.')
            # Redirect back to the view_orders page
            return redirect('view_orders')
    else:
        form = OrderEditForm(instance=order)

    context = {'order': order, 'form': form}
    return render(request, 'edit_order.html', context)





def delete_order(request):
    if request.method == 'GET':
        transaction_id = request.GET.get('transaction_id')
        order = get_object_or_404(Order, transaction_id=transaction_id)
        order.delete()
        return redirect('view_orders')
    else:
        return redirect('view_orders')  # Handle non-GET requests as needed
    




def view_shipping_address(request, transaction_id):
    order = get_object_or_404(Order, transaction_id=transaction_id)
    shipping_address = order.shipping

    return render(request, 'view_shipping_address.html', {'shipping_address': shipping_address})







@login_required(login_url="users:login")
def view_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, "view_user.html", {"user": user})



def user_list(request):
    users = User.objects.all()
    return render(request, "user_list.html", {"users": users})


# @login_required(login_url="users:login")
# def edit_user(request, user_id):
#     user = get_object_or_404(User, id=user_id)

#     if request.method == 'POST':
#         form = UserEditForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('view_user', user_id=user_id)
#     else:
#         form = UserEditForm(instance=user)

#     return render(request, "edit_user.html", {"form": form, "user": user})










@login_required(login_url="users:login")
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User details updated successfully.')
            return redirect('users:user_list')
    else:
        form = UserEditForm(instance=user)

    return render(request, "edit_user.html", {"form": form, "user": user})











@login_required(login_url="users:login")
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('users:user_list')










def directions(request):
    if request.user.is_authenticated:
        return render(request, "directions.html")
    else:
        return redirect("store/templates:homebase")
    
















# Driver view and edit views


def driver_view_orders(request):
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'driver_view_order.html', context)

# --------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------


def driver_edit_order(request, transaction_id):
    order = get_object_or_404(Order, transaction_id=transaction_id)

    if request.method == 'POST':
        form = OrderEditForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            # Add a success message
            messages.success(request, 'successful.')
            # Redirect back to the driver_view_orders page
            return redirect('driver_view_orders')
    else:
        form = OrderEditForm(instance=order)

    context = {'order': order, 'form': form}
    return render(request, 'driver_edit_order.html', context)




def driver_view_shipping_address(request, transaction_id):
    order = get_object_or_404(Order, transaction_id=transaction_id)
    shipping_address = order.shipping

    return render(request, 'driver_view_shipping_address.html', {'shipping_address': shipping_address})
