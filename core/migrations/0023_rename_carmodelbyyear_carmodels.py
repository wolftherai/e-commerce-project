# Generated by Django 4.0.3 on 2022-05-23 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_oempart_remove_carmodelbyyear_products_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CarModelByYear',
            new_name='CarModels',
        ),
    ]
