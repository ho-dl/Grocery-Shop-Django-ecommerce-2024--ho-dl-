from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from APP.models import Product , Slider
from django.core.files.storage import default_storage 

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Cart
from django.shortcuts import get_object_or_404, redirect
from .models import Product, Cart
from .models import Product, Order, OrderItem, Cart
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem, Cart  # Ensure correct import

# Your views here


from django.shortcuts import get_object_or_404, redirect, render
from .models import Product, Cart
from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem, Cart, Product
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from django.contrib import messages
from .models import Order, OrderItem, Cart, Product
from decimal import Decimal

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from .decorators import admin_required
from django.core.paginator import Paginator





@login_required
def place_order(request):
    if request.method == 'POST':
        # Extract form data
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # Retrieve user's cart
        try:
            cart = Cart.objects.get(user=request.user)
            products_in_cart = cart.products.all()

            # Calculate total amount
            total_amount = Decimal('0.00')
            for cart_item in products_in_cart:
                product = cart_item  # Ensure this is correct, assuming cart_item is already a Product instance
                price = product.price
                quantity = cart_item.quantity
                total_amount += price * Decimal(quantity)

            # Create Order instance
            order = Order.objects.create(user=request.user, total_amount=total_amount,
                                         email=email, phone=phone, address=address)

            # Create OrderItem instances for each product in the cart
            for cart_item in products_in_cart:
                product = cart_item  # Ensure this is correct, assuming cart_item is already a Product instance
                quantity = cart_item.quantity
                OrderItem.objects.create(order=order, product=product, quantity=quantity)

            # Clear the cart after placing the order
            cart.products.clear()

            return render(request, 'order_placed.html', {'order': order})
        
        except Cart.DoesNotExist:
            messages.error(request, "Cart does not exist.")
            return redirect('checkout')  # Redirect to checkout page or any appropriate page

    else:
        return render(request, 'checkout.html')
    


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        # Delete the order from the database
        order.delete()
        
        # Optionally, add a message indicating successful cancellation
        messages.success(request, f"Order #{order.id} has been cancelled and deleted.")
        
        # Redirect to a success page or reload the my_orders page
        return redirect('my_orders')
    
    # Handle GET request (usually to confirm cancellation)
    context = {
        'order': order
    }
    return render(request, 'cancel_order.html', context)



@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    context = {
        'orders': orders
    }
    return render(request, 'my_orders.html', context)

def update_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        new_quantity = request.POST.get('quantity')
        product.quantity = new_quantity
        product.save()
    return redirect('view_cart')  # Redirect back to cart after updating quantity

@login_required
def checkout(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    products = user_cart.products.all()
    return render(request, 'checkout.html', {'products': products})

@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    user_cart = Cart.objects.get(user=request.user)  # Assuming you have a Cart model related to users
    user_cart.products.remove(product)
    return redirect('view_cart')  # Redirect back to the cart page after removal

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    user_cart.products.add(product)
    return redirect('index')  # Redirect to index or any other page after adding to cart

@login_required
def view_cart(request):
    user_cart, created = Cart.objects.get_or_create(user=request.user)
    products = user_cart.products.all()
    return render(request, 'cart.html', {'products': products})
    
# Your other views can remain unchanged


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        phone_number = request.POST['phone_number']
        
        # Validate passwords match
        if password != confirm_password:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
        
        # Create a new user
        user = User.objects.create_user(username=username, password=password)
        
        # Create a profile for the user
        profile = Profile(user=user, phone_number=phone_number)
        profile.save()

        # Redirect to login page or any other page after successful registration
        return redirect('login')  # Adjust 'login' to the name of your login URL
    else:
        return render(request, 'register.html')





def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to index page after login
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'login.html')



def register_view(request):
    return render(request, 'register.html')

def index(request):
    products_list = Product.objects.all()
    
    paginator = Paginator(products_list, 8)  # Show 8 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    sliders = Slider.objects.all()
    
    return render(request, 'index.html', {'address': page_obj, 'sliders': sliders})

@admin_required
def dashboard(request):
    dashboard_address = Product.objects.all()
    return render(request, 'dashboard.html', {'dashboard_address': dashboard_address})



def category_view(request, category):
    products = Product.objects.filter(category=category)
    return render(request, f'{category.lower()}.html', {'products': products})


def fruits(request):
    fruits_list = Product.objects.filter(category='FRU')
    
    paginator = Paginator(fruits_list, 8)  # Show 8 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'fruits.html', {'address': page_obj})


def vegitables(request):
    vegitables_list = Product.objects.filter(category='VEG')
    
    paginator = Paginator(vegitables_list, 8)  # Show 8 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'vegitables.html', {'address': page_obj})


def icecream(request):
    icecreams_list = Product.objects.filter(category='ICE')

    paginator = Paginator(icecreams_list, 8)  # Show 8 ice creams per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'icecream.html', {'icecreams': page_obj})

def groceries(request):
    groceries_list = Product.objects.filter(category='GRO')
    
    paginator = Paginator(groceries_list, 8)  # Show 8 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'grocery.html', {'address': page_obj})


@admin_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.quantity = request.POST.get('quantity')
        product.category = request.POST.get('category')

        if 'image' in request.FILES:
            if product.images:
                if default_storage.exists(product.images.path):
                    default_storage.delete(product.images.path)
            product.images = request.FILES['image']

        product.save()
        return redirect('dashboard')
    
    return render(request, 'edit.html', {'product': product})

    
    return render(request, 'edit.html', {'person': person})
@admin_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    return redirect('dashboard')

@admin_required
def upload_content(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        category = request.POST.get('category')
        image = request.FILES.get('image')

        person = Product.objects.create(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            category=category,
            images=image
        )

        return redirect('dashboard')
    else:
        return render(request, 'upload.html')
