from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('welcome_app.urls')),  # Include the URLs from welcome_app
]
