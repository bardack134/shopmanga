# Generated by Django 3.2 on 2023-09-07 02:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_categoriajp_productojp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productojp',
            name='category',
        ),
        migrations.DeleteModel(
            name='CategoriaJP',
        ),
        migrations.DeleteModel(
            name='ProductoJP',
        ),
    ]
