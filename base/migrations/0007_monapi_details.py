# Generated by Django 2.0.1 on 2020-07-16 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_monapi_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='monapi',
            name='details',
            field=models.TextField(null=True),
        ),
    ]
