# Generated by Django 3.1.4 on 2021-07-23 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psdf_main', '0037_auto_20210722_0723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appraisal_admin',
            name='apprdate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='monitoring_admin',
            name='monidate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='projects',
            name='appraprdate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='projects',
            name='approvedate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='projects',
            name='denydate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='projects',
            name='dpraprdate',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='projects',
            name='dprsubdate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='projects',
            name='finalaprdate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='projects',
            name='moniaprdate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='projects',
            name='tesgaprdate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='temp_projects',
            name='dprdenydate',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='temp_projects',
            name='dprsubdate',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='tesg_admin',
            name='TESG_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='tesg_master',
            name='user_res_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='aprdate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='reqdate',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]