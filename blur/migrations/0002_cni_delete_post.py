# Generated by Django 5.0.6 on 2024-07-06 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blur', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CNI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(default='###', max_length=10)),
                ('identication', models.PositiveIntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
