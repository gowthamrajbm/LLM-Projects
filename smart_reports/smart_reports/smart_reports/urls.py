"""
URL configuration for smart_reports project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views  # Import your views module

urlpatterns = [
    path('', views.home_view, name='home'),  # For function-based view
    path('admin/', admin.site.urls),
    path('search_query/', views.search_query, name='search_query'),
    # path('', HomeView.as_view(), name='home'),  # Uncomment for class-based view
]
