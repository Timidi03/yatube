# Generated by Django 5.0.3 on 2024-04-01 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_cd_group_post_group'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CD',
        ),
        migrations.AlterField(
            model_name='group',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
