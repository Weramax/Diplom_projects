# Generated by Django 2.0.3 on 2018-04-02 20:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projectpage', '0005_auto_20180401_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='created_task',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Дата создания'),
            preserve_default=False,
        ),
    ]