# Generated by Django 4.1.3 on 2023-12-05 19:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_task_worker_response'),
        ('notifications', '0004_alter_tasknotification_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasknotification',
            name='task',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='task.task'),
        ),
    ]
