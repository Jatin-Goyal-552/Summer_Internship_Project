# Generated by Django 3.2.5 on 2022-06-21 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api2', '0003_auto_20220621_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expertise',
            name='last_used',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
