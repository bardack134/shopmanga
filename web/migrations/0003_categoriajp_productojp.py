# Generated by Django 3.2 on 2023-09-06 23:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_producto_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaJP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'CategoriaJP',
                'verbose_name_plural': 'CategoriasJP',
            },
        ),
        migrations.CreateModel(
            name='ProductoJP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('availability', models.BooleanField(default=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='productos')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='web.categoriajp')),
            ],
            options={
                'verbose_name': 'ProductoJP',
                'verbose_name_plural': 'ProductosJP',
            },
        ),
    ]
