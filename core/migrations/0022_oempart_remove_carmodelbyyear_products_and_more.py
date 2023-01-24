# Generated by Django 4.0.3 on 2022-05-23 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_carmodelbyyear'),
    ]

    operations = [
        migrations.CreateModel(
            name='OemPart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=12, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='carmodelbyyear',
            name='products',
        ),
        migrations.AddField(
            model_name='carmodelbyyear',
            name='oem_parts',
            field=models.ManyToManyField(to='core.oempart'),
        ),
    ]