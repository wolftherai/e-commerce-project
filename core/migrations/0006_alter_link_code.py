# Generated by Django 4.0.3 on 2022-05-10 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_brand_category_manufacturer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='code',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
