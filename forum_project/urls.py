# forum_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('forum.urls')),  # Laad de URL's van de forum app
    # Gebruik de standaard Django login view, maar stel een custom template in:
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    
    
]
