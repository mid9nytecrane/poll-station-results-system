# Generated by Django 5.0.7 on 2024-09-03 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='pollStations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ps_name', models.CharField(max_length=50)),
                ('ps_code', models.CharField(max_length=50)),
                ('serial_num', models.IntegerField()),
                ('reg_voters', models.IntegerField()),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
