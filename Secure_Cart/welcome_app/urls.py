from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    welcome_page,
    login_view,
    signup_view,
    all_users_view,
    update_profile_view,
    admin_dashboard,
    orders,
)
from . import views

from .views import homepage, manage_products, delete_product
from .views import add_to_basket, view_basket
from .views import buy_now
urlpatterns = [
    # the welcome page which anyone can get to
    path('', welcome_page, name='welcome'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    # a homepage for users who've logged in
    path('homepage/', homepage, name='homepage'),
    # a sign-up page for customers
    path('signup/', signup_view, name='signup'),
    # the admin only dashboard
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    # the admin only view of all the available customers
    path('all-users/', all_users_view, name='all_users'),
    # updates the profile of a customer
    path('update-profile/', update_profile_view, name='update_profile'),
    path('manage-products/', manage_products, name='manage_products'),
    path('delete-product/<int:product_id>/', delete_product, name='delete_product'),
    path('add-to-basket/<int:product_id>/', add_to_basket, name='add_to_basket'),
    path('basket/', view_basket, name='view_basket'),
    path('remove-from-basket/<int:item_id>/', views.remove_from_basket, name='remove_from_basket'),
    path('buy-now/', buy_now, name='buy_now'),
    path('orders/', orders, name='orders'),
    path('remove-order/<int:order_id>/', views.remove_order, name='remove_order'),
    path('verify-security-question/', views.verify_security_question, name='verify_security_question'),
]