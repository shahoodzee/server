# Generated by Django 4.1.3 on 2023-11-25 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_client_cnic'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='task_count',
            field=models.IntegerField(null=True),
        ),
    ]
