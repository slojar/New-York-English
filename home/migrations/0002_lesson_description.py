# Generated by Django 4.2.11 on 2024-05-18 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
