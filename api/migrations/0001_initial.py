# Generated by Django 4.2.7 on 2023-11-24 00:33

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=100, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/brands/')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_order', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(11), django.core.validators.MaxLengthValidator(11)])),
                ('address', models.CharField(max_length=300)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('in the way', 'in the way'), ('arrived', 'arrived'), ('cancelled', 'cancelled')], default='pending', max_length=500)),
                ('total_coast', models.FloatField(blank=True, default=0, null=True)),
                ('created_date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=100, unique=True)),
                ('description', models.TextField()),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('updated_date', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.category')),
                ('related', models.ManyToManyField(blank=True, null=True, to='api.product')),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('shipping_price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(db_index=True, max_length=100, unique=True)),
                ('email', models.CharField(db_index=True, max_length=300, unique=True)),
                ('password', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(8)])),
            ],
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buy_price', models.FloatField(default=0)),
                ('sell_price', models.FloatField(default=0)),
                ('before_discount', models.FloatField(blank=True, default=0, null=True)),
                ('earning', models.FloatField(blank=True, default=0, null=True)),
                ('stock_quantity', models.IntegerField(default=0)),
                ('height', models.CharField(blank=True, max_length=100, null=True)),
                ('weight', models.CharField(blank=True, max_length=100, null=True)),
                ('size', models.CharField(choices=[('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('2X', '2X'), ('3X', '3X')], max_length=200, null=True)),
                ('purchased_times', models.IntegerField(blank=True, default=0, null=True)),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.brand')),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.color')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_variant', to='api.product')),
            ],
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_requierd', models.CharField(choices=[('no', 'no'), ('yes', 'yes'), ('in making order', 'in making order')], default='no', max_length=300)),
                ('category_image_1', models.ImageField(blank=True, null=True, upload_to='categories/images/')),
                ('category_image_2', models.ImageField(blank=True, null=True, upload_to='categories/images/')),
                ('category_image_3', models.ImageField(blank=True, null=True, upload_to='categories/images/')),
                ('category_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category1', to='api.category')),
                ('category_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category2', to='api.category')),
                ('category_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category3', to='api.category')),
                ('new', models.ManyToManyField(blank=True, null=True, related_name='product_new', to='api.product')),
                ('popular', models.ManyToManyField(blank=True, null=True, related_name='product_popular', to='api.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(null=True, upload_to='products/images/')),
                ('alt', models.CharField(blank=True, max_length=100, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='api.product')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_items', to='api.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.product')),
                ('variant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.variant')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.state'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.user'),
        ),
        migrations.CreateModel(
            name='Landing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_up', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=80)),
                ('image', models.ImageField(upload_to='images/landing/images/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.category')),
                ('setting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='setting_landing', to='api.settings')),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.product')),
                ('variant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.variant')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user'),
        ),
    ]
