# Generated by Django 5.1.1 on 2024-10-25 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0006_alter_aggregateforecast_centers_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="question_weight",
            field=models.FloatField(default=1.0),
        ),
    ]
