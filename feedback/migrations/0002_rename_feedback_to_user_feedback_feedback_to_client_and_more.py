# Generated by Django 4.1.3 on 2023-11-18 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='feedback',
            old_name='feedback_to_user',
            new_name='feedback_to_client',
        ),
        migrations.AddField(
            model_name='feedback',
            name='client_feedback_status',
            field=models.CharField(choices=[('Given', 'Given'), ('Pending', 'Pending')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='feedback',
            name='task_experience',
            field=models.CharField(choices=[('Best', 'Best'), ('Good', 'Good'), ('Satisfied', 'Satisfied'), ('Bad', 'Bad'), ('Worst', 'Worst')], default='Pending', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='feedback',
            name='worker_feedback_status',
            field=models.CharField(choices=[('Given', 'Given'), ('Pending', 'Pending')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='feedback_to_worker',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
