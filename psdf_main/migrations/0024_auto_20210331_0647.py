# Generated by Django 3.1.4 on 2021-03-31 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psdf_main', '0023_auto_20210322_0812'),
    ]

    operations = [
        migrations.AddField(
            model_name='tesg',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='tesg_admin',
            name='TESG_date',
            field=models.DateTimeField(null=True),
        ),
    ]
