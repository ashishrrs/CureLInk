# Generated by Django 4.0.4 on 2022-05-04 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=10)),
                ('email_id', models.CharField(blank=True, max_length=100)),
                ('subscriptions', models.ManyToManyField(blank=True, related_name='Topic', to='user_management.topic')),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(null=True)),
                ('notification_time', models.TimeField()),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_management.topic')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
