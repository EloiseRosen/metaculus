# Generated by Django 5.0.6 on 2024-07-01 14:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0024_alter_post_maybe_try_to_resolve_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="maybe_try_to_resolve_at",
            field=models.DateTimeField(
                db_index=True,
                default=datetime.datetime(
                    2064, 6, 21, 14, 32, 52, 688644, tzinfo=datetime.timezone.utc
                ),
            ),
        ),
    ]