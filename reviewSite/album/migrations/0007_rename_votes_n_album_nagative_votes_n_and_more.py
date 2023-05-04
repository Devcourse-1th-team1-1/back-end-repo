# Generated by Django 4.2 on 2023-05-04 06:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('album', '0006_merge_20230504_1224'),
    ]

    operations = [
        migrations.RenameField(
            model_name='album',
            old_name='votes_n',
            new_name='nagative_votes_n',
        ),
        migrations.RenameField(
            model_name='album',
            old_name='voters',
            new_name='positive_voters',
        ),
        migrations.AddField(
            model_name='album',
            name='negative_voters',
            field=models.ManyToManyField(related_name='disliked_albums', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='album',
            name='positive_votes_n',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
