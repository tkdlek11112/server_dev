# Generated by Django 3.0.5 on 2020-08-15 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_auto_20200815_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loginuser',
            name='user_pw',
            field=models.CharField(default=False, max_length=255),
        ),
    ]
