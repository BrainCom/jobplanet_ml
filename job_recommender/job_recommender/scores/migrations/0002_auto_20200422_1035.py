# Generated by Django 3.0.5 on 2020-04-22 01:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scores', '0001_initial'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='companysimilarity',
            name='scores_comp_source__6d6129_idx',
        ),
        migrations.RemoveIndex(
            model_name='customersimilarity',
            name='scores_cust_source__3e91b7_idx',
        ),
    ]
