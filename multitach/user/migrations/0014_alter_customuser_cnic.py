# Generated by Django 4.1.3 on 2024-01-09 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_alter_customuser_cnic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='cnic',
            field=models.BigIntegerField(null=True),
        ),
    ]
