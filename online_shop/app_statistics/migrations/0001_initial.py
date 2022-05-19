# Generated by Django 3.2 on 2022-05-19 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_goods', '0001_initial'),
        ('app_orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='quantity')),
                ('dt', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_orders.orders', verbose_name='date of sale')),
                ('goodsidx', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statistics', to='app_goods.goods', verbose_name='goods')),
            ],
            options={
                'verbose_name': 'statistic',
                'verbose_name_plural': 'statistics',
            },
        ),
    ]
