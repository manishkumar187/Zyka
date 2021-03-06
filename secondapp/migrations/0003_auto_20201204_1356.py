# Generated by Django 3.0.6 on 2020-12-04 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secondapp', '0002_contact_us'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_name', models.CharField(max_length=250)),
                ('cover_pic', models.FileField(upload_to='media/%Y/%m/%d')),
                ('description', models.TextField()),
                ('added_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='contact_us',
            options={'verbose_name_plural': 'contact_us'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name_plural': 'Student'},
        ),
    ]
