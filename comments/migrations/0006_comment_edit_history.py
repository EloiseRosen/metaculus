# Generated by Django 5.0.6 on 2024-06-27 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0005_remove_comment_type_comment_is_private'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='edit_history',
            field=models.JSONField(default=list),
        ),
    ]