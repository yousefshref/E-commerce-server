from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, validate_integer
from colorfield.fields import ColorField


class User(models.Model):
    username = models.CharField(max_length=100, unique=True, db_index=True)
    email = models.CharField(max_length=300, unique=True, db_index=True)
    password = models.CharField(max_length=100, validators=[
                                MinLengthValidator(8)])

    def __str__(self):
        return self.username


class ProductImage(models.Model):
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/images/', null=True)
    alt = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.alt)


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        return str(self.title)+str(self.id)


class Brand(models.Model):
    title = models.CharField(max_length=100, unique=True, db_index=True)
    image = models.ImageField(
        upload_to='images/brands/', null=True, blank=True)

    def __str__(self):
        return str(self.title)+str(self.id)


class Color(models.Model):
    color = ColorField()

    def __str__(self):
        return str(self.color)+str(self.id)


sizes = (
    ("XS", "XS"),
    ("S", "S"),
    ("M", "M"),
    ("L", "L"),
    ("XL", "XL"),
    ("2X", "2X"),
    ("3X", "3X"),
)


class Product(models.Model):
    title = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, null=True, blank=True)
    related = models.ManyToManyField("Product", null=True, blank=True)
    purchased_times = models.IntegerField(null=True, blank=True, default=0)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # purchased times
        variants = Variant.objects.filter(product__id=self.pk)
        v = []
        for i in variants:
            v.append(int(i.purchased_times))
        self.purchased_times = sum(v)

        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title)


class Variant(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_variant')

    title = models.CharField(max_length=100, default="__")

    buy_price = models.FloatField(default=0)
    sell_price = models.FloatField(default=0)
    before_discount = models.FloatField(null=True, blank=True, default=0)
    earning = models.FloatField(null=True, blank=True, default=0)

    stock_quantity = models.IntegerField(default=0)

    color = models.ForeignKey(
        Color, on_delete=models.CASCADE, null=True, blank=True)

    purchased_times = models.IntegerField(null=True, blank=True, default=0)

    def save(self, *args, **kwargs):
        # earning
        self.earning = self.sell_price - self.buy_price

        # stock handle
        if self.stock_quantity == 0:
            raise Exception('No Enough Stock')

        # purchased tiems check
        items = OrderItem.objects.filter(product__id=self.product.pk)
        value = []
        for i in items:
            value.append(i.quantity)
        if sum(value) == self.purchased_times:
            pass
        else:
            self.purchased_times = sum(value)

        super(Variant, self).save(*args, **kwargs)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_order = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.user)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    created_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(CartItem, self).save(*args, **kwargs)

        prices = []
        carts = CartItem.objects.filter(cart__pk=self.cart.pk)
        for i in carts:
            prices.append(i.variant.sell_price * i.quantity)

        self.cart.total_order = sum(prices)
        self.cart.save()

    def __str__(self):
        return str(self.cart)


class State(models.Model):
    name = models.CharField(max_length=100)
    shipping_price = models.FloatField()

    def __str__(self):
        return str(self.name)

# {
# "user":"1",
# "name":"test",
# "phone":"12312312312",
# "address":"test address",
# "state":"1",
# "order_items":[
#      {
#       "product":3,
#       "quantity":2
#      }
#   ]
# }


status_choices = (
    ("pending", "pending"),
    ("in the way", "in the way"),
    ("arrived", "arrived"),
    ("cancelled", "cancelled"),
)


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, validators=[
                             MinLengthValidator(11), MaxLengthValidator(11)])
    address = models.CharField(max_length=300)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=500, choices=status_choices, default="pending")

    total_coast = models.FloatField(default=0, null=True, blank=True)
    created_date = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        # total coas
        values = []
        items = OrderItem.objects.filter(order__id=self.pk)
        for i in items:
            values.append(i.variant.sell_price * i.quantity)
        self.total_coast = sum(values)+self.state.shipping_price
        super(Order, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        items = OrderItem.objects.filter(order__id=self.pk)
        for i in items:
            i.variant.stock_quantity += i.quantity
            i.variant.save()
        super(Order, self).delete(*args, **kwargs)

    def __str__(self):
        return str(self.user)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='order_items', null=True, blank=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()

    def save(self, *args, **kwargs):
        if self.variant.stock_quantity - self.quantity < 0:
            raise Exception('No Enough Stock')

        # remove stock from prduct
        try:
            old_quantity = OrderItem.objects.get(id=self.pk).quantity
        except:
            old_quantity = 0
        new_quantity = self.quantity

        quantity = old_quantity - new_quantity

        self.variant.stock_quantity = self.variant.stock_quantity + quantity
        self.variant.save()

        super(OrderItem, self).save(*args, **kwargs)
        # save total coast
        self.order.save()

        self.variant.save()

    def delete(self, *args, **kwargs):
        self.variant.stock_quantity += self.quantity
        self.variant.save()
        super(OrderItem, self).delete(*args, **kwargs)
        self.order.save()

    def __str__(self):
        return str(self.order)


choices_login = (
    ("no", "no"),
    ("yes", "yes"),
    ("in making order", "in making order"),
)


class Settings(models.Model):
    login_requierd = models.CharField(
        choices=choices_login, max_length=300, default="no")

    category_1 = models.ForeignKey(
        Category, related_name='category1', null=True, blank=True, on_delete=models.CASCADE)
    category_image_1 = models.ImageField(
        upload_to='categories/images/', null=True, blank=True)

    category_2 = models.ForeignKey(
        Category, related_name='category2', null=True, blank=True, on_delete=models.CASCADE)
    category_image_2 = models.ImageField(
        upload_to='categories/images/', null=True, blank=True)

    category_3 = models.ForeignKey(
        Category, related_name='category3', null=True, blank=True, on_delete=models.CASCADE)
    category_image_3 = models.ImageField(
        upload_to='categories/images/', null=True, blank=True)

    new = models.ManyToManyField(
        Product, null=True, blank=True, related_name='product_new')
    popular = models.ManyToManyField(
        Product, null=True, blank=True, related_name='product_popular')


class Landing(models.Model):
    setting = models.ForeignKey(
        Settings, on_delete=models.CASCADE, related_name='setting_landing')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title_up = models.CharField(max_length=50)
    title = models.CharField(max_length=80)
    image = models.ImageField(upload_to='images/landing/images/')
