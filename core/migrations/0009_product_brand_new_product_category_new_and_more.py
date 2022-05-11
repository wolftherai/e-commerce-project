# Generated by Django 4.0.3 on 2022-05-10 23:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_product_manufacturer_new'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand_new',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.brand'),
        ),
        migrations.AddField(
            model_name='product',
            name='category_new',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='manufacturer_new',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='manufacturer_id', to='core.manufacturer'),
        ),
    ]
