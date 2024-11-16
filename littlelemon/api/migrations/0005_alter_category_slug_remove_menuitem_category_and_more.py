# Generated by Django 4.2.16 on 2024-11-06 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_category_image_alter_menuitem_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='category',
        ),
        migrations.AddField(
            model_name='menuitem',
            name='category',
            field=models.ManyToManyField(related_name='items', to='api.category'),
        ),
    ]
