# Generated by Django 3.0.6 on 2020-12-16 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('secondapp', '0008_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='course_ids',
            new_name='product_ids',
        ),
    ]