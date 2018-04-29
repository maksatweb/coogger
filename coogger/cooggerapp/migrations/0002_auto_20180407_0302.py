# Generated by Django 2.0 on 2018-04-07 00:02

from django.db import migrations, models
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('cooggerapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='upvote',
            field=models.BooleanField(default=False, verbose_name='was voting done'),
        ),
        migrations.AlterField(
            model_name='content',
            name='content',
            field=martor.models.MartorField(),
        ),
        migrations.AlterField(
            model_name='otherinformationofusers',
            name='about',
            field=martor.models.MartorField(default=True),
            preserve_default=False,
        ),
    ]