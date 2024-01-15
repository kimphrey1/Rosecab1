from django.contrib import admin
from django.urls import path
from custom_admin.views import *
from django.conf import settings
from django.conf.urls.static import static

# forgot edit size and delete size, so those functions do not work yet, just buttons


urlpatterns = [
    path('admin/', admin.site.urls),

    # Admin login
    path('admin-login/', adminLogin, name="admin_login"),

    # Admin home
    path('adminhome/', adminHome, name="adminhome"),

    # Dashboard
    path('admindashboard/', admin_dashboard, name="admindashboard"),
    
    # category
    path('add-category/', add_category, name="add_category"),
    path('view-category/', view_category, name="view_category"),
    path('edit-category/<int:pid>/', edit_category, name="edit_category"),
    path('delete-category/<int:pid>/', delete_category, name="delete_category"),


    # size
    path('add-size/', add_size, name="add_size"), 
    path('view-size/', view_size, name="view_size"),
        # testing
    path('edit-size/<int:pid>/', edit_size, name="edit_size"),
    path('delete-size/<int:pid>/', delete_size, name="delete_size"),

    
    
    # Product
    path('add-product/', add_product, name='add_product'),

    path('view-product/', view_product, name='view_product'),

    path('edit-product/<uuid:pid>/', edit_product, name="edit_product"),

    path('delete-product/<uuid:pid>/', delete_product, name="delete_product"),


    # Product variants
    path('view-product-variants/', view_product_variants, name='view_product_variants'),
    path('add-product-variant/', add_productvariant, name='add_productvariant'),
    path('edit-productvariant/<int:variant_id>/', edit_productvariant, name='edit_productvariant'),
    path('delete-productvariant/<uuid:pid>/', delete_productvariant, name='delete_productvariant'),






    # Orders
    path('view_order/', view_orders, name='view_orders'),


    path('edit_order/<uuid:transaction_id>/', edit_order, name='edit_order'),

    path('delete_order/', delete_order, name='delete_order'), 


    path('view-shipping-address/<uuid:transaction_id>/', view_shipping_address, name='view_shipping_address'),





    

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)