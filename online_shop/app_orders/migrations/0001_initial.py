# Generated by Django 3.2 on 2022-05-19 09:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_goods', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountsRules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentdiscount', models.IntegerField(default=0, verbose_name='percent discount')),
                ('normaldiscount', models.IntegerField(default=1, verbose_name='normal discount')),
                ('fixedprice', models.IntegerField(default=2, verbose_name='fixed price')),
            ],
            options={
                'verbose_name': 'discount rule',
                'verbose_name_plural': 'discounts rules',
            },
        ),
        migrations.CreateModel(
            name='GoodsSets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goodsset', models.TextField(verbose_name='goods set')),
                ('setdiscount', models.FloatField(verbose_name='set discount')),
                ('discountruleidx', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_orders.discountsrules', verbose_name='discount rule')),
                ('goodsidx', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sets', to='app_goods.goods', verbose_name='goods')),
            ],
            options={
                'verbose_name': 'goods set',
                'verbose_name_plural': 'goods sets',
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card', models.IntegerField(default=0, verbose_name='card number')),
                ('foreignaccount', models.IntegerField(default=1, verbose_name='foreign account')),
            ],
            options={
                'verbose_name': 'payment rule',
                'verbose_name_plural': 'payment methods',
            },
        ),
        migrations.CreateModel(
            name='ShipmentMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('normal', models.IntegerField(default=0, verbose_name='normal shipping method ')),
                ('express', models.IntegerField(default=1, verbose_name='express shipping method')),
            ],
            options={
                'verbose_name': 'shipment method',
                'verbose_name_plural': 'shipment methods',
            },
        ),
        migrations.CreateModel(
            name='ShipmentRules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('freenormal', models.FloatField(default=2000, verbose_name='free shipping')),
                ('paidnormal', models.FloatField(default=200, verbose_name='standard shipping')),
                ('paidexpress', models.FloatField(default=500, verbose_name='express shipping')),
            ],
            options={
                'verbose_name': 'shipment rule',
                'verbose_name_plural': 'shipment rules',
            },
        ),
        migrations.CreateModel(
            name='SetsDiscountsCalendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startdt', models.DateTimeField(verbose_name='start date')),
                ('enddt', models.DateTimeField(verbose_name='end date')),
                ('isactive', models.BooleanField(verbose_name='active')),
                ('setidx', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_orders.goodssets', verbose_name='goods')),
            ],
            options={
                'verbose_name': 'set discount calendar',
                'verbose_name_plural': 'sets discounts calendar',
            },
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.TextField(verbose_name='order list')),
                ('dt', models.DateTimeField(auto_now=True, verbose_name='order date')),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=8, verbose_name='order total price')),
                ('address', models.CharField(max_length=50, verbose_name='order delivery address')),
                ('paid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_orders.paymentmethod', verbose_name='payment method')),
                ('shipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_orders.shipmentmethod', verbose_name='shipment method')),
                ('useridx', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orderitem', to='app_goods.goods', verbose_name='orderitem')),
                ('orderidx', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_orders.orders', verbose_name='order')),
            ],
            options={
                'verbose_name': 'order item',
                'verbose_name_plural': 'order items',
            },
        ),
        migrations.CreateModel(
            name='GoodsDiscountsCalendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startdt', models.DateTimeField(verbose_name='start date')),
                ('enddt', models.DateTimeField(verbose_name='end date')),
                ('isactive', models.BooleanField(verbose_name='is active')),
                ('goodsidx', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_goods.goods', verbose_name='goods')),
            ],
            options={
                'verbose_name': 'goods discount calendar',
                'verbose_name_plural': 'goods discounts calendar',
            },
        ),
        migrations.CreateModel(
            name='GoodsDiscounts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goodsdiscount', models.FloatField(verbose_name='goods discount')),
                ('discountruleidx', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_orders.discountsrules', verbose_name='discount rule')),
                ('goodsidx', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='discounts', to='app_goods.goods', verbose_name='goods')),
            ],
            options={
                'verbose_name': 'goods discount',
                'verbose_name_plural': 'goods discounts',
            },
        ),
    ]
