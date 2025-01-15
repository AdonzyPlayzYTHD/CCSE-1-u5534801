from django.contrib import admin
from welcome_app.models import Profile
from welcome_app.models import Product

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'surname', 'address', 'postcode')

admin.site.register(Product)