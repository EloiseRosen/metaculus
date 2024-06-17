# Generated by Django 5.0.6 on 2024-06-14 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0003_alter_post_approved_at_alter_post_approved_by_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="closed_at",
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AddField(
            model_name="post",
            name="curation_status",
            field=models.CharField(
                choices=[
                    ("draft", "Draft"),
                    ("pending", "Pending"),
                    ("rejected", "Rejected"),
                    ("published", "Published"),
                    ("closed", "Closed"),
                ],
                default="draft",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="rejected_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]