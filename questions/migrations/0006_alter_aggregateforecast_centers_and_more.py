# Generated by Django 5.1.1 on 2024-10-22 13:21

import django_better_admin_arrayfield.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "questions",
            "0005_remove_aggregateforecast_questions_a_questio_0d22f0_idx_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="aggregateforecast",
            name="centers",
            field=django_better_admin_arrayfield.models.fields.ArrayField(
                base_field=models.FloatField(), null=True, size=None
            ),
        ),
        migrations.AlterField(
            model_name="aggregateforecast",
            name="forecast_values",
            field=django_better_admin_arrayfield.models.fields.ArrayField(
                base_field=models.FloatField(), max_length=201, size=None
            ),
        ),
        migrations.AlterField(
            model_name="aggregateforecast",
            name="histogram",
            field=django_better_admin_arrayfield.models.fields.ArrayField(
                base_field=models.FloatField(), null=True, size=100
            ),
        ),
        migrations.AlterField(
            model_name="aggregateforecast",
            name="interval_lower_bounds",
            field=django_better_admin_arrayfield.models.fields.ArrayField(
                base_field=models.FloatField(), null=True, size=None
            ),
        ),
        migrations.AlterField(
            model_name="aggregateforecast",
            name="interval_upper_bounds",
            field=django_better_admin_arrayfield.models.fields.ArrayField(
                base_field=models.FloatField(), null=True, size=None
            ),
        ),
        migrations.AlterField(
            model_name="aggregateforecast",
            name="means",
            field=django_better_admin_arrayfield.models.fields.ArrayField(
                base_field=models.FloatField(), null=True, size=None
            ),
        ),
        migrations.AlterField(
            model_name="forecast",
            name="continuous_cdf",
            field=django_better_admin_arrayfield.models.fields.ArrayField(
                base_field=models.FloatField(), null=True, size=201
            ),
        ),
        migrations.AlterField(
            model_name="forecast",
            name="distribution_components",
            field=django_better_admin_arrayfield.models.fields.ArrayField(
                base_field=models.JSONField(null=True),
                help_text="The components for a continuous prediction. Used to generate prediction_values.",
                null=True,
                size=5,
            ),
        ),
        migrations.AlterField(
            model_name="forecast",
            name="probability_yes_per_category",
            field=django_better_admin_arrayfield.models.fields.ArrayField(
                base_field=models.FloatField(), null=True, size=None
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="options",
            field=django_better_admin_arrayfield.models.fields.ArrayField(
                base_field=models.CharField(max_length=200),
                blank=True,
                null=True,
                size=None,
            ),
        ),
    ]