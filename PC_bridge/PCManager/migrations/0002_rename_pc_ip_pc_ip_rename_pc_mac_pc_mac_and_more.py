# Generated by Django 4.0.6 on 2022-07-11 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PCManager', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pc',
            old_name='pc_ip',
            new_name='ip',
        ),
        migrations.RenameField(
            model_name='pc',
            old_name='pc_mac',
            new_name='mac',
        ),
        migrations.RenameField(
            model_name='pc',
            old_name='pc_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='pc',
            old_name='pc_id',
            new_name='pcid',
        ),
    ]
