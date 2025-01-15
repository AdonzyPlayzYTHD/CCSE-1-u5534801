from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django import forms
from .models import Profile, Product, Basket, BasketItem, Order, OrderItem
from django.http import Http404
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


class ProductForm(forms.ModelForm): # the products form class showing the attributes associated with each product
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'inventory']


@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request): # The admins dashboard
    current_year = datetime.now().year
    return render(request, 'welcome_app/admin_dashboard.html', {'current_year': current_year})

# Manage Products
@user_passes_test(lambda u: u.is_superuser)
def manage_products(request): #Shows the class for the admin the addition of products
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Product added successfully!")
        return redirect('manage_products')

    products = Product.objects.all()
    return render(request, 'welcome_app/manage_products.html', {'form': form, 'products': products})


@user_passes_test(lambda u: u.is_superuser)
def delete_product(request, product_id): # shows the class of the admin deleting a product
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect('manage_products')

def welcome_page(request): # the view showing the welcome page where all users are welcomed before being asked to sign in
    return render(request, 'welcome_app/welcome.html')


def login_view(request):# the login view where users are asked to login adn enter their credentials
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('verify_security_question')  # Correct redirection
        messages.error(request, "Invalid username or password.")
    return render(request, 'welcome_app/login.html')


@login_required # shows only authorised users are allowed to get this far
def homepage(request):
    products = Product.objects.all()
    return render(request, 'welcome_app/homepage.html', {'products': products})


SECURITY_QUESTIONS = [ # the security questions users will be asked after trying to login, a second line of defence
    "What is your mother's maiden name?",
    "What was the name of your first pet?",
    "What is your favorite book?",
    "What city were you born in?",
]

def signup_view(request): # a signup view showing the details which users need to enter when trying to signuo and create an account
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        surname = request.POST.get('surname')
        address = request.POST.get('address')
        postcode = request.POST.get('postcode')
        security_question = request.POST.get('security_question')
        security_answer = request.POST.get('security_answer')

        # validation for passwords
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')
        # validation for the strength of a password
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long!")
            return redirect('signup')

        # assures that the user name is not already taken
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')

        # the creation of a new users profile
        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.create(
            user=user,
            first_name=first_name,
            surname=surname,
            address=address,
            postcode=postcode,
            security_question=request.POST.get('security_question'),
            security_answer=request.POST.get('security_answer'),
        )

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'welcome_app/signup.html', {'security_questions': SECURITY_QUESTIONS})

@login_required
def update_profile_view(request): # function needed for when a user wants to update their profile
    user = request.user
    profile = get_object_or_404(Profile, user=user)

    if request.method == 'POST':
        # updates the user
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        if request.POST.get('password'):
            user.set_password(request.POST['password'])
        user.save()

        # updates the users profile
        profile.first_name = request.POST.get('first_name', profile.first_name)
        profile.surname = request.POST.get('surname', profile.surname)
        profile.address = request.POST.get('address', profile.address)
        profile.postcode = request.POST.get('postcode', profile.postcode)
        profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('homepage')

    return render(request, 'welcome_app/update_profile.html', {'user': user, 'profile': profile})

@user_passes_test(lambda u: u.is_superuser) # ensures that only the admin can access this function and view all of the users information
def all_users_view(request):
    users_with_orders = []

    for user in User.objects.all():
        orders = Order.objects.filter(user=user)
        users_with_orders.append({
            'user': user,
            'orders': orders
        })

    return render(request, 'welcome_app/all_users.html', {'users_with_orders': users_with_orders})
@login_required
def add_to_basket(request, product_id): # the function of how customers can add items to their basket
    product = get_object_or_404(Product, id=product_id)

    # makes sure that the product is in stock before adding it to the customers basket
    if product.inventory <= 0:
        messages.error(request, "This product is out of stock!")
        return redirect('homepage')

    basket, created = Basket.objects.get_or_create(user=request.user)
    basket_item, created = BasketItem.objects.get_or_create(basket=basket, product=product)

    # decreases the stock value by 1 once its added to a customers basket
    product.inventory -= 1
    product.save()

    if not created:
        basket_item.quantity += 1
    basket_item.save()

    messages.success(request, "Product added to basket.")
    return redirect('homepage')

@login_required
def view_basket(request): # allows for customers to view the items which they have added to their basket
    basket, _ = Basket.objects.get_or_create(user=request.user)
    return render(request, 'welcome_app/basket.html', {'basket': basket})

@login_required
def remove_from_basket(request, item_id): # customers are allowed to remove items from their baskets
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        basket_item = BasketItem.objects.get(id=item_id, basket__user=request.user)
        basket_item.delete()
    except BasketItem.DoesNotExist:
        raise Http404("No BasketItem matches the given query.")

    return redirect('view_basket')

@login_required
def buy_now(request):# once added to the basket, customers are now able to checkout and buy the products which they added
    basket = get_object_or_404(Basket, user=request.user)
    if not basket.items.exists():
        messages.error(request, "Your basket is empty!")
        return redirect('view_basket')

    # makes sure again that the stock is available before allowing them to buy the products
    for item in basket.items.all():
        if item.product.inventory < item.quantity:
            messages.error(request, f"Not enough stock for {item.product.name}.")
            return redirect('view_basket')

    # reduce stock value
    total_price = sum(item.quantity * item.product.price for item in basket.items.all())
    order = Order.objects.create(user=request.user, total_price=total_price)
    OrderItem.objects.bulk_create([
        OrderItem(order=order, product=item.product, quantity=item.quantity)
        for item in basket.items.all()
    ])
    for item in basket.items.all():
        item.product.inventory -= item.quantity
        item.product.save()

    # clears the basket ready for them to buy more products
    basket.items.all().delete()
    messages.success(request, "Order placed successfully!")
    return redirect('orders')

@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'welcome_app/orders.html', {'orders': orders})
@login_required
def remove_order(request, order_id):
    # makes sure that that order belongs to the signed in user
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # deletes the order
    order.delete()

    messages.success(request, "Order successfully removed.")
    return redirect('orders')  # once deleted the user is redirected back to the orders page


@login_required
def verify_security_question(request):
    # checks if user is the admin
    if request.user.is_superuser:
        return redirect('admin_dashboard')

    # gets the customers profile
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return redirect('login')  # returns to login page if information is incorrect

    if request.method == 'POST':
        security_answer = request.POST.get('security_answer', '').strip().lower()
        if security_answer == profile.security_answer.lower():
            return redirect('homepage')  # redirects to homepage if it is correct
        else:
            messages.error(request, "Incorrect security answer. Please try again.")

    return render(request, 'welcome_app/verify_security_question.html', {'security_question': profile.security_question})
