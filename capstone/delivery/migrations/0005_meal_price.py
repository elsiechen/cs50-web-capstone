# Generated by Django 3.2.7 on 2022-02-25 02:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0004_auto_20220215_0502'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]