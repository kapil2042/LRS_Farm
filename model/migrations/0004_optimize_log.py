# Generated by Django 4.0.5 on 2022-10-13 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0003_delete_userdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='optimize_log',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_count', models.IntegerField()),
                ('date', models.DateField()),
            ],
        ),
    ]
