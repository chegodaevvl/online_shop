# Generated by Django 3.2 on 2022-05-19 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banners',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advertisementname', models.CharField(max_length=50, verbose_name='advertiser')),
                ('bannerimg', models.ImageField(default=None, null=True, upload_to='img/', verbose_name='banner image')),
                ('isactive', models.BooleanField(default=False, verbose_name='active')),
                ('bannerlink', models.TextField(verbose_name='banner link')),
            ],
            options={
                'verbose_name': 'banner',
                'verbose_name_plural': 'banners',
            },
        ),
    ]
