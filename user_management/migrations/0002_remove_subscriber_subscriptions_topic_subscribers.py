# Generated by Django 4.0.4 on 2022-05-05 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriber',
            name='subscriptions',
        ),
        migrations.AddField(
            model_name='topic',
            name='subscribers',
            field=models.ManyToManyField(blank=True, related_name='Subscriber', to='user_management.subscriber'),
        ),
    ]