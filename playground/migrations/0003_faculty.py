# Generated by Django 4.0.2 on 2022-05-15 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0002_seatingplan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=130)),
                ('Post', models.CharField(max_length=130)),
            ],
        ),
    ]