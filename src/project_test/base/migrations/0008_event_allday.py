# Generated by Django 5.1.3 on 2025-03-18 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_remove_event_time_remove_event_user_event_created_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='allDay',
            field=models.BooleanField(default=False),
        ),
    ]
