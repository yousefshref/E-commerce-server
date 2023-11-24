from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import serializers
from . import models
from django.db.models import Q
from django.http import JsonResponse
from faker import Faker
import random
import urllib.request
import os
from rest_framework.pagination import PageNumberPagination
from django.views.decorators.cache import cache_page

# products = [
#     {"title": "Smart Fitness Tracker", "description": "Track your fitness goals and monitor health metrics with this sleek smart fitness tracker.", "buy_price": 40, "sell_price": 79.99},
#     {"title": "Wireless Charging Mouse Pad", "description": "Stay productive and charge your devices simultaneously with this innovative wireless charging mouse pad.", "buy_price": 25, "sell_price": 49.99},
#     {"title": "Portable Solar Power Bank", "description": "Charge your devices on the go with this portable solar-powered power bank.", "buy_price": 30, "sell_price": 59.99},
#     {"title": "Smart LED Desk Lamp", "description": "Illuminate your workspace with adjustable brightness and color temperature using this smart LED desk lamp.", "buy_price": 35, "sell_price": 69.99},
#     {"title": "Digital Drawing Tablet", "description": "Unleash your creativity with precision using this high-performance digital drawing tablet.", "buy_price": 70, "sell_price": 129.99},
#     {"title": "Wireless Sport Earphones", "description": "Enjoy your workouts with these wireless sport earphones providing immersive sound and comfort.", "buy_price": 50, "sell_price": 99.99},
#     {"title": "Compact Air Purifier", "description": "Breathe clean air in small spaces with this compact and efficient air purifier.", "buy_price": 40, "sell_price": 79.99},
#     {"title": "Smart Home Security Camera", "description": "Monitor your home with HD video and smart detection features using this security camera.", "buy_price": 60, "sell_price": 119.99},
#     {"title": "Stylish Laptop Backpack", "description": "Carry your laptop and essentials in style with this modern and spacious laptop backpack.", "buy_price": 45, "sell_price": 89.99},
#     {"title": "Digital Nomad Essentials Kit", "description": "Stay organized and productive on the go with this kit tailored for digital nomads.", "buy_price": 80, "sell_price": 149.99},
#     {"title": "Smart Home Thermostat", "description": "Control your home's temperature remotely and save energy with this smart thermostat.", "buy_price": 55, "sell_price": 109.99},
#     {"title": "Premium Noise-Canceling Headphones", "description": "Immerse yourself in music and silence with these premium noise-canceling headphones.", "buy_price": 100, "sell_price": 199.99},
#     {"title": "Wireless Charging Desk Organizer", "description": "Declutter your workspace and charge your devices with this multifunctional wireless charging desk organizer.", "buy_price": 70, "sell_price": 129.99},
#     {"title": "Gourmet Cooking Utensil Set", "description": "Elevate your culinary experience with this premium set of gourmet cooking utensils.", "buy_price": 55, "sell_price": 109.99},
#     {"title": "Digital Alarm Clock with Wireless Charger", "description": "Wake up in style and charge your phone wirelessly with this modern digital alarm clock.", "buy_price": 30, "sell_price": 59.99},
#     {"title": "Smart Doorbell Camera", "description": "Enhance your home security with this smart doorbell camera featuring real-time video and two-way communication.", "buy_price": 120, "sell_price": 249.99},
#     {"title": "Outdoor Adventure Hammock", "description": "Relax and unwind outdoors with this durable and comfortable outdoor adventure hammock.", "buy_price": 40, "sell_price": 79.99},
#     {"title": "Digital Instant Print Camera", "description": "Capture and print memories instantly with this easy-to-use digital instant print camera.", "buy_price": 50, "sell_price": 99.99},
#     {"title": "Smart Bluetooth Water Bottle", "description": "Stay hydrated and track your water intake with this smart Bluetooth-enabled water bottle.", "buy_price": 25, "sell_price": 49.99},
#     {"title": "High-Performance Gaming Mouse", "description": "Gain a competitive edge with this high-performance gaming mouse designed for precision and speed.", "buy_price": 35, "sell_price": 69.99},
#     {"title": "Foldable Laptop Stand", "description": "Create an ergonomic workspace on the go with this foldable and adjustable laptop stand.", "buy_price": 20, "sell_price": 39.99},
#     {"title": "Premium Leather Wallet", "description": "Organize your essentials in style with this premium leather wallet featuring multiple card slots and a sleek design.", "buy_price": 30, "sell_price": 59.99},
#     {"title": "Smart Plant Monitoring Kit", "description": "Take care of your plants with this smart plant monitoring kit that tracks soil moisture, light, and temperature.", "buy_price": 45, "sell_price": 89.99},
#     {"title": "Digital Fitness Scale", "description": "Track your fitness progress with precision using this digital fitness scale with a sleek and modern design.", "buy_price": 25, "sell_price": 49.99},
#     {"title": "Portable Espresso Maker", "description": "Enjoy your favorite coffee beverages on the go with this compact and portable espresso maker.", "buy_price": 60, "sell_price": 119.99},
#     {"title": "Smart Wi-Fi Light Bulbs", "description": "Illuminate your space and set the mood with these smart Wi-Fi-enabled light bulbs controllable via smartphone.", "buy_price": 30, "sell_price": 59.99},
#     {"title": "Premium Leather Desk Set", "description": "Upgrade your workspace with this premium leather desk set including a mouse pad, pen holder, and coaster.", "buy_price": 40, "sell_price": 79.99},
#     {"title": "Wireless Sport Headphones", "description": "Experience freedom and high-quality sound during your workouts with these wireless sport headphones.", "buy_price": 50, "sell_price": 99.99},
#     {"title": "Smart Home Door Lock", "description": "Enhance your home security with this smart door lock that offers keyless entry and remote control capabilities.", "buy_price": 90, "sell_price": 179.99},
# ]
# create product
    # titles = []
    # for i in products:
    #     titles.append(i['title'])

    # des = []
    # for i in products:
    #     des.append(i['description'])

    # b = []
    # for i in products:
    #     b.append(i['buy_price'])

    # s = []
    # for i in products:
    #     s.append(i['sell_price'])

    # cate = [8, 10, 11]
    # cate_ins = models.Category.objects.get(id=random.choice(cate))

    # br = [13, 14, 15]
    # br_ins = models.Brand.objects.get(id=random.choice(br))

    # colors = [5, 6, 7, 8, 9]
    # color_ins = models.Color.objects.get(id=random.choice(colors))

    # stock_qty = []
    # for i in str(5000):
    #     stock_qty.append(i)

    # stock = [10, 15, 20, 5]

    # i = 0
    # while i < 30:
    #     i = i + 1
    #     new = models.Product(
    #         title=random.sample(titles, 17)[0],
    #         description=random.choice(des),
    #         buy_price=random.choice(b),
    #         sell_price=random.choice(s),
    #         category=cate_ins,
    #         brand=br_ins,
    #         color=color_ins,
    #         stock_quantity=random.choice(stock),
    #     ).save()
"""
TEST
"""
def get_image_url():
    return f"https://picsum.photos/500/500"


@api_view(['POST'])
def test(request):
    fake = Faker()
    # download image
    try:
        # products = models.Product.objects.all()
        # for i in products:
            # urllib.request.urlretrieve(get_image_url(), f'D:/projects/one time systems/E-commerce/back/products/images/{i.title+".png"}')
            # models.ProductImage(
            #     product=i,
            #     image=f'D:/projects/one time systems/E-commerce/back/products/images/{i.title+".png"}',
            #     alt=i.title,
            # ).save()
            # i.save()
        
        print('sucess')

    except Exception as e:
        print(f"Failed to download image. Error: {e}")



    return Response({"":""})






"""
Auth
"""
@api_view(['POST'])
def register(request):
    ser = serializers.UserSerializer(data=request.data)
    if ser.is_valid():
        ser.save()
        # create cart
        try:
            cart = models.Cart.objects.get(user__id=ser.data['id'])
            pass
        except:
            user_insta = models.User.objects.get(id=ser.data['id'])

            cart_create = models.Cart(
                user=user_insta
            ).save()
        # create cart
        return Response(ser.data)
    return Response(ser.errors)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        exist = models.User.objects.get(username=username)
        if exist.password == password:
            # create cart
            try:
                cart = models.Cart.objects.get(user__id=exist.pk)
                pass
            except:
                user_insta = models.User.objects.get(id=exist.pk)

                cart_create = models.Cart(
                    user=user_insta
                ).save()
            # create cart
            return Response({"success":exist.pk})

        else:
            return Response({"password":"Password is wrong"})
    except:
            return Response({"error":"No user with this username"})



@api_view(['GET'])
def get_user(request):
    user = models.User.objects.get(id=request.GET.get('id'))
    ser = serializers.UserSerializer(user)
    return Response(ser.data)


@api_view(['GET'])
def get_auth_settings(request):
    settings = models.Settings.objects.all()
    ser = serializers.SettingsSerializer(settings, many=True)
    return Response(ser.data)


"""
Category
"""
@api_view(['GET'])
def get_categories(request):
    categories = models.Category.objects.all()
    ser = serializers.CategorySerializer(categories, many=True)
    return Response(ser.data)

"""
Brand
"""
@api_view(['GET'])
def get_brands(request):
    brands = models.Brand.objects.all()
    ser = serializers.BrandSerializer(brands,many=True)
    return Response(ser.data)


"""
State
"""
@api_view(['GET'])
def get_states(request):
    categories = models.State.objects.all()
    ser = serializers.StateSerializer(categories, many=True)
    return Response(ser.data)


"""
Product
"""
# @cache_page(60 * 15)
@api_view(['GET'])
def get_products(request):
    category_filter = request.GET.get('category')
    brand_filter = request.GET.get('brand')
    search = request.GET.get('search')

    products = models.Product.objects.all().order_by('-id').order_by('-purchased_times')

    if category_filter:
        products = products.filter(category__id=category_filter)

    if brand_filter:
        products = products.filter(brand__id=brand_filter)


    if search:
        words = search.split(' ')
        q_objects = [Q(title__icontains=word) | Q(description__icontains=word) for word in words]

        combined_q_object = Q()
        for q_object in q_objects:
            combined_q_object |= q_object

        products = products.filter(combined_q_object)

    ser = serializers.ProductSerializer(products, many=True)
    return Response(ser.data)


@api_view(['GET'])
def get_product(request, pk):
    product = models.Product.objects.get(id=pk)
    ser = serializers.ProductSerializer(product)
    return Response(ser.data)


@api_view(['GET'])
def get_variants(request):
    variants = models.Variant.objects.all()
    ser = serializers.VariantSerializer(variants, many=True)
    return Response(ser.data)




"""
Cart
"""
@api_view(['POST'])
def create_or_update_cart(request):
    user_id = request.GET.get('user_id')
    product = request.data.get('product')
    variant = request.data.get('variant')
    quantity = request.data.get('quantity')

    try:
        cart = models.CartItem.objects.get(cart__user__id=user_id, product__id=product, variant__id=variant)
        # # update
        cart.quantity = quantity
        cart.save()
        return Response({"success":True})
    except:
        # create
        ca = models.Cart.objects.get(user__id=user_id)
        pr = models.Product.objects.get(id=product)
        vr = models.Variant.objects.get(id=variant)
        models.CartItem(
            cart=ca,
            product=pr,
            variant=vr,
            quantity=quantity
        ).save()
        return Response({"success":True})



@api_view(['GET'])
def get_cart(request):
    user_id = request.GET.get('user_id')

    cart = models.CartItem.objects.filter(cart__user__id=user_id)

    ser = serializers.CartItemSerializer(cart, many=True)

    return Response(ser.data)


@api_view(['DELETE'])
def delete_cart_item(request, pk):
    item = models.CartItem.objects.get(id=pk)

    item.delete()

    print(pk)

    return Response({"success":True})


@api_view(['DELETE'])
def delete_cart_items(request):
    items = models.CartItem.objects.filter(cart__user__id=request.GET.get('id'))
    
    for i in items:
        i.delete()

    return Response({"success":True})



"""
Orders
"""
# create order
@api_view(['POST'])
def create_order(request):
    data = request.data

    ser = serializers.OrderSerializer(data=data)

    if ser.is_valid():
        ser.save()
        print(ser.data['id'])
        return Response(ser.data)

    return Response(ser.errors)


@api_view(['GET'])
def get_orders(request, pk):
    orders = models.Order.objects.filter(user__id=pk).order_by('-id')

    ser = serializers.OrderSerializer(orders, many=True)

    return Response(ser.data)




