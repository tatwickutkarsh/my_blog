# Generated by Django 3.0.8 on 2020-08-09 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20200809_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='attach_photo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='posts'),
        ),
    ]
