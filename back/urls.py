from django.contrib import admin
from django.urls import path
from api import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('admin/', admin.site.urls),

    path('test/', views.test),

    # auth
    path('register/', views.register),
    path('login/', views.login),
    path('get_user/', views.get_user),
    path('get_auth_settings/', views.get_auth_settings),


    # categories
    path('get_categories/', views.get_categories),

    # states
    path('get_states/', views.get_states),

    # brands
    path('get_brands/', views.get_brands),


    # products
    path('get_products/', views.get_products),
    path('get_product/<int:pk>', views.get_product),
    path('get_variants/', views.get_variants),


    # cart
    path('create_or_update_cart/', views.create_or_update_cart),
    path('get_cart/', views.get_cart),
    path('delete_cart_item/<int:pk>', views.delete_cart_item),
    path('delete_cart_items/', views.delete_cart_items),


    # order
    path('create_order/', views.create_order),
    path('get_orders/<int:pk>', views.get_orders),



]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)