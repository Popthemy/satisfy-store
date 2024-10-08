# Generated by Django 4.2.6 on 2024-08-25 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_address_zip_code'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'verbose_name': 'Address', 'verbose_name_plural': 'Addresses'},
        ),
        migrations.AddField(
            model_name='address',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default='2024-08-25 17:36'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
