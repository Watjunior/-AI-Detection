# Generated by Django 5.0.6 on 2024-07-06 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blur', '0002_cni_delete_post'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cni',
            old_name='identication',
            new_name='ident',
        ),
        migrations.AddField(
            model_name='cni',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
