# Generated by Django 5.1.3 on 2024-11-29 22:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_emailbatch_sender_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emailbatch',
            name='sender_email',
        ),
    ]