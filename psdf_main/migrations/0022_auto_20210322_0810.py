# Generated by Django 3.1.4 on 2021-03-22 08:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('psdf_main', '0021_auto_20210317_0933'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='a_tesg',
            name='projid',
        ),
        migrations.RemoveField(
            model_name='tesg',
            name='project',
        ),
        migrations.RemoveField(
            model_name='u_tesg',
            name='projid',
        ),
        migrations.DeleteModel(
            name='projects',
        ),
    ]
