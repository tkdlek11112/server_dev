# Generated by Django 3.0.5 on 2020-08-15 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LoginUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default=False, max_length=20)),
                ('user_pw', models.CharField(default=False, max_length=20)),
            ],
            options={
                'verbose_name': '로그인 테스트 테이블',
                'db_table': 'login_user',
            },
        ),
    ]