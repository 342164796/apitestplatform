# Generated by Django 2.0.1 on 2020-01-10 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20190813_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interface',
            name='method',
            field=models.CharField(max_length=20),
        ),
    ]