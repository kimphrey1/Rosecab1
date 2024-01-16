from django.urls import path
from . import views
from custom_admin.views import view_user
from custom_admin.views import user_list
from custom_admin.views import edit_user
from custom_admin.views import delete_user
app_name = "users"

urlpatterns = [
    path("register/", views.SignUpView.as_view(), name="register"),
    path("login/", views.MyLoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("orders/", views.my_orders, name="my_orders"),


    # added from custom_admin
    path('user_list/', user_list, name='user_list'),
    path('view_user/<int:user_id>/', view_user, name='view_user'),
     path('edit_user/<int:user_id>/', edit_user, name='edit_user'),
     path('delete_user/<int:user_id>/', delete_user, name='delete_user'),
]
