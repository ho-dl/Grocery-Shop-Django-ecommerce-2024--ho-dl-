from django.urls import path
from APP import views
from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib.auth.decorators import login_required  # Import login_required decorator
from APP import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('category/<str:category>/', views.category_view, name='category_view'),
    path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('upload/', views.upload_content, name='upload_content'),
    path('vegitable/',views.vegitables,name='vegitables'),
    path('fruits/', views.fruits, name='fruits'),
    path('icecream/', views.icecream, name='icecream'),
    path('grocery/', views.groceries, name='grocery'),


    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),

    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),

     path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('update_cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('place_order/', views.place_order, name='place_order'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('my-orders/', views.my_orders, name='my_orders'),

    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),


    
    


    
]


# <a href="{% url 'fruits' %}">Fruits</a>
# <a href="{% url 'icecream' %}">Ice Cream</a>
# <a href="{% url 'grocery' %}">Groceries</a>
# <a href="{% url 'vegitable' %}">Groceries</a>


