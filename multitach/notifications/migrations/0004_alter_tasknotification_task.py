# Generated by Django 4.1.3 on 2023-12-05 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_task_worker_response'),
        ('notifications', '0003_alter_tasknotification_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasknotification',
            name='task',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='task.task'),
        ),
    ]
