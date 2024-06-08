"""
URL configuration for Qwicky project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from app1 import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home1'),
    path('home',views.home,name='home'),
    path('allproducts',views.allproducts,name='allproducts'),
    path('aboutus',views.aboutus,name='aboutus'),
    path('contactus',views.contactus,name='contactus'),
    path('contactus/add_record',views.add_record,name='add_record'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('search',views.search,name='search'),
    path('signup',views.signupuser,name='signup'),
    path('login',views.loginuser,name='login'),
    path('logout',views.logoutuser,name='logout'),
    path('profile',views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('add_wishlists',views.add_wishlists,name='add_wishlists'),
    path('cart',views.add_to_cart,name='cart'),
    path('<int:pid>', views.details, name='details'),
    path('show_wishlists',views.show_wishlists, name='show_wishlists'),
    path('show_cart',views.show_cart,name='show_cart'),
    path('remove_item_cart',views.remove_item_cart,name='remove_item_cart'),
    path('remove_item_wishlist',views.remove_item_wishlist,name='remove_item_wishlist'),
    path('update_cart',views.update_cart, name='update_cart'),
    path('calculate_bill', views.calculate_bill,name='calculate_bill'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    
]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
