# Generated by Django 3.0.8 on 2020-08-09 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20200809_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='edited_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]