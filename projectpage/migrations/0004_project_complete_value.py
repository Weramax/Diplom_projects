# Generated by Django 2.0.3 on 2018-05-03 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectpage', '0003_documents_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='complete_value',
            field=models.CharField(default=0, max_length=1),
            preserve_default=False,
        ),
    ]
