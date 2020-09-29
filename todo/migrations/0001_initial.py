# Generated by Django 3.0.5 on 2020-09-29 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(default=False, max_length=20, unique=True)),
                ('name', models.DateField(null=True, verbose_name='작업이름')),
                ('start_date', models.DateField(null=True, verbose_name='시작날짜')),
                ('end_date', models.DateField(null=True, verbose_name='마감날짜')),
                ('finish_date', models.DateField(null=True, verbose_name='완료날짜')),
                ('state', models.IntegerField(default=0, verbose_name='상태')),
            ],
            options={
                'verbose_name': '작업(to-do) 테이블',
                'db_table': 'task',
            },
        ),
    ]
