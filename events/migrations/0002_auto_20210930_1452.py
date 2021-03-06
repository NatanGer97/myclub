# Generated by Django 3.2.7 on 2021-09-30 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venue',
            name='address',
            field=models.CharField(blank=True, max_length=300, verbose_name='Venue name'),
        ),
        migrations.AlterField(
            model_name='venue',
            name='email_address',
            field=models.EmailField(blank=True, max_length=254, verbose_name='Email Address'),
        ),
        migrations.AlterField(
            model_name='venue',
            name='name',
            field=models.CharField(blank=True, max_length=120, verbose_name='Venue name'),
        ),
        migrations.AlterField(
            model_name='venue',
            name='phone',
            field=models.CharField(blank=True, max_length=25, verbose_name='Contact Phone'),
        ),
        migrations.AlterField(
            model_name='venue',
            name='web',
            field=models.URLField(blank=True, verbose_name='Website Address'),
        ),
        migrations.AlterField(
            model_name='venue',
            name='zip_code',
            field=models.CharField(blank=True, max_length=15, verbose_name='Zip Code'),
        ),
    ]
