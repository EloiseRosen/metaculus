# Generated by Django 5.0.6 on 2024-06-28 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0009_alter_post_projects"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="rejected_at",
        ),
        migrations.AddField(
            model_name="post",
            name="curation_status_updated_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="post",
            name="resolved_at",
            field=models.DateTimeField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name="post",
            name="curation_status",
            field=models.CharField(
                choices=[
                    ("draft", "Draft"),
                    ("pending", "Pending"),
                    ("rejected", "Rejected"),
                    ("approved", "Approved"),
                    ("deleted", "Deleted"),
                ],
                db_index=True,
                default="draft",
                max_length=20,
            ),
        ),
    ]