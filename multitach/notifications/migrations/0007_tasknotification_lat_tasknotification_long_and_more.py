# Generated by Django 5.0.1 on 2024-01-15 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0006_remove_tasknotification_message_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasknotification',
            name='lat',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='tasknotification',
            name='long',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='tasknotification',
            name='status',
            field=models.CharField(choices=[('TaskPost', 'TaskPosted'), ('TaskAccept', 'TaskAccepted'), ('TaskProcessing', 'TaskProcessing'), ('TaskDeclined', 'TaskDeclined'), ('TaskCompleted', 'TaskCompleted')], default='TaskPosted', max_length=20),
        ),
        migrations.AddField(
            model_name='tasknotification',
            name='taskType',
            field=models.CharField(choices=[('Electrician', 'Electrician'), ('Plumber', 'Plumber'), ('Carpenter', 'Carpenter'), ('Goldsmith', 'Goldsmith'), ('Blacksmith', 'Blacksmith'), ('Other', 'Other')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='tasknotification',
            name='text_address',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='tasknotification',
            name='time',
            field=models.TimeField(null=True),
        ),
    ]