# Generated by Django 5.0.6 on 2024-07-01 18:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0033_alter_post_maybe_try_to_resolve_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="maybe_try_to_resolve_at",
            field=models.DateTimeField(
                db_index=True,
                default=datetime.datetime(
                    2064, 6, 21, 18, 22, 5, 67423, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
    ]