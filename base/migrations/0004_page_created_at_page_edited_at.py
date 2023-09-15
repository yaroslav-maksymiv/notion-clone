# Generated by Django 4.2 on 2023-06-28 19:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_page_name_alter_page_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='page',
            name='edited_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]