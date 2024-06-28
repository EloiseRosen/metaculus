from dataclasses import dataclass
from datetime import datetime

from scipy.stats.mstats import gmean
import numpy as np

from questions.models import Forecast, Question
from scoring.models import Score


@dataclass
class AggregationEntry:
    pmf: np.ndarray
    num_forecasters: int
    timestamp: float


def get_geometric_means(
    forecasts: list[Forecast],
) -> list[AggregationEntry]:
    geometric_means = []
    timesteps: set[datetime] = set()
    for forecast in forecasts:
        timesteps.add(forecast.start_time.timestamp())
        if forecast.end_time:
            timesteps.add(forecast.end_time.timestamp())
    for timestep in sorted(timesteps):
        prediction_values = [
            f.get_pmf()
            for f in forecasts
            if f.start_time.timestamp() <= timestep
            and (f.end_time is None or f.end_time.timestamp() >= timestep)
        ]
        if not prediction_values:
            continue  # TODO: doesn't account for going from 1 active forecast to 0
        geometric_mean = gmean(prediction_values, axis=0)
        predictors = len(prediction_values)
        geometric_means.append(
            AggregationEntry(
                geometric_mean, predictors if predictors > 1 else 0, timestep
            )
        )
    return geometric_means


def get_medians(
    forecasts: list[Forecast],
) -> list[AggregationEntry]:
    medians = []
    timesteps: set[datetime] = set()
    for forecast in forecasts:
        timesteps.add(forecast.start_time.timestamp())
        if forecast.end_time:
            timesteps.add(forecast.end_time.timestamp())
    for timestep in sorted(timesteps):
        prediction_values = [
            f.get_pmf()
            for f in forecasts
            if f.start_time.timestamp() <= timestep
            and (f.end_time is None or f.end_time.timestamp() >= timestep)
        ]
        if not prediction_values:
            continue  # TODO: doesn't account for going from 1 active forecast to 0
        median = np.median(prediction_values, axis=0)
        predictors = len(prediction_values)
        medians.append(
            AggregationEntry(median, predictors if predictors > 1 else 0, timestep)
        )
    return medians


@dataclass
class ForecastScore:
    score: float
    coverage: float = 0


def evaluate_forecasts_baseline_accuracy(
    forecasts: list[Forecast],
    resolution_bucket: int,
    window_start: float,
    window_end: float,
    question_type: str,
    open_bounds_count: int,
) -> list[ForecastScore]:
    total_duration = window_end - window_start
    forecast_scores: list[tuple[float, float]] = []
    for forecast in forecasts:
        forecast_start = max(forecast.start_time.timestamp(), window_start)
        if forecast.end_time:
            forecast_end = min(forecast.end_time.timestamp(), window_end)
        else:
            forecast_end = window_end
        forecast_duration = forecast_end - forecast_start
        if not forecast_duration:
            forecast_scores.append(ForecastScore(0))
            continue
        forecast_coverage = forecast_duration / total_duration
        pmf = forecast.get_pmf()
        if question_type in ["binary", "multiple_choice"]:
            forecast_score = (
                100 * np.log(pmf[resolution_bucket] * len(pmf)) / np.log(len(pmf))
            )
        else:
            if resolution_bucket in [0, len(pmf) - 1]:
                baseline = 0.05
            else:
                baseline = (1 - 0.05 * open_bounds_count) / (len(pmf) - 2)
            forecast_score = 100 * np.log(pmf[resolution_bucket] * baseline) / 2
        forecast_scores.append(
            ForecastScore(forecast_score * forecast_coverage, forecast_coverage)
        )

    return forecast_scores


def evaluate_forecasts_baseline_spot_forecast(
    forecasts: list[Forecast],
    resolution_bucket: int,
    spot_forecast_timestamp: float,
    question_type: str,
    open_bounds_count: int,
) -> list[ForecastScore]:
    forecast_scores: list[float] = []
    for forecast in forecasts:
        start = forecast.start_time.timestamp()
        end = (
            float("inf") if forecast.end_time is None else forecast.end_time.timestamp()
        )
        if start <= spot_forecast_timestamp < end:
            pmf = forecast.get_pmf()
            if question_type in ["binary", "multiple_choice"]:
                forecast_score = (
                    100 * np.log(pmf[resolution_bucket] * len(pmf)) / np.log(len(pmf))
                )
            else:
                if resolution_bucket in [0, len(pmf) - 1]:
                    baseline = 0.05
                else:
                    baseline = (1 - 0.05 * open_bounds_count) / (len(pmf) - 2)
                forecast_score = 100 * np.log(pmf[resolution_bucket] * baseline) / 2
            forecast_scores.append(ForecastScore(forecast_score))
        else:
            forecast_scores.append(ForecastScore(0))
    return forecast_scores


def evaluate_forecasts_peer_accuracy(
    forecasts: list[Forecast],
    resolution_bucket: int,
    window_start: float,
    window_end: float,
    question_type: str,
) -> list[ForecastScore]:
    geometric_means = get_geometric_means(forecasts)
    total_duration = window_end - window_start
    forecast_scores: list[float] = []
    for forecast in forecasts:
        forecast_start = max(forecast.start_time.timestamp(), window_start)
        if forecast.end_time:
            forecast_end = min(forecast.end_time.timestamp(), window_end)
        else:
            forecast_end = window_end
        if (forecast_end - forecast_start) <= 0:
            forecast_scores.append(ForecastScore(0))
            continue

        pmf = forecast.get_pmf()
        interval_scores = []
        for gm in geometric_means:
            if forecast_start <= gm.timestamp < forecast_end:
                score = (
                    100
                    * (gm.num_forecasters / (gm.num_forecasters - 1))
                    * np.log(pmf[resolution_bucket] / gm.pmf[resolution_bucket])
                )
                if question_type in ["numeric", "date"]:
                    score /= 2
                interval_scores.append(score)
            else:
                interval_scores.append(0)

        forecast_score = 0
        forecast_coverage = 0
        times = [
            gm.timestamp for gm in geometric_means if gm.timestamp < window_end
        ] + [window_end]
        for i in range(len(times) - 1):
            interval_duration = times[i + 1] - times[i]
            forecast_score += interval_scores[i] * interval_duration / total_duration
            forecast_coverage += interval_duration / total_duration
        forecast_scores.append(ForecastScore(forecast_score, forecast_coverage))

    return forecast_scores


def evaluate_forecasts_peer_spot_forecast(
    forecasts: list[Forecast],
    resolution_bucket: int,
    spot_forecast_timestamp: float,
    question_type: str,
) -> list[ForecastScore]:
    geometric_mean_forecasts = get_geometric_means(forecasts)
    g = None
    for gm in geometric_mean_forecasts[::-1]:
        if gm.timestamp < spot_forecast_timestamp:
            g = gm.pmf
            break
    if g is None:
        return [ForecastScore(0)] * len(forecasts)

    forecast_scores: list[float] = []
    for forecast in forecasts:
        start = forecast.start_time.timestamp()
        end = (
            float("inf") if forecast.end_time is None else forecast.end_time.timestamp()
        )
        if start <= spot_forecast_timestamp < end:
            pmf = forecast.get_pmf()
            forecast_score = (
                100
                * (gm.num_forecasters / (gm.num_forecasters - 1))
                * np.log(pmf[resolution_bucket] / gm.pmf[resolution_bucket])
            )
            if question_type in ["numeric", "date"]:
                forecast_score /= 2
            forecast_scores.append(ForecastScore(forecast_score))
        else:
            forecast_scores.append(ForecastScore(0))
    return forecast_scores


def evaluate_forecasts_legacy_relative(
    forecasts: list[Forecast],
    resolution_bucket: int,
    window_start: float,
    window_end: float,
    question_type: str,
) -> list[ForecastScore]:
    return [ForecastScore(0)] * len(forecasts)  # not yet implemented


def evaluate_question(
    question: Question,
    resolution_bucket: int,
    score_type: str,
    spot_forecast_timestamp: float | None = None,
) -> list[Score]:
    window_start = question.post.published_at.timestamp()
    window_end = question.closed_at.timestamp()

    forecasts = question.forecast_set.all()

    score_types = Score.ScoreTypes
    match score_type:
        case score_types.BASELINE:
            open_bounds_count = bool(question.open_upper_bound) + bool(
                question.open_lower_bound
            )
            forecast_scores = evaluate_forecasts_baseline_accuracy(
                forecasts,
                resolution_bucket,
                window_start,
                window_end,
                question.type,
                open_bounds_count,
            )
        case score_types.SPOT_BASELINE:
            open_bounds_count = bool(question.open_upper_bound) + bool(
                question.open_lower_bound
            )
            forecast_scores = evaluate_forecasts_baseline_spot_forecast(
                forecasts,
                resolution_bucket,
                spot_forecast_timestamp,
                question.type,
                open_bounds_count,
            )
        case score_types.PEER:
            forecast_scores = evaluate_forecasts_peer_accuracy(
                forecasts,
                resolution_bucket,
                window_start,
                window_end,
                question.type,
            )
        case score_types.SPOT_PEER:
            forecast_scores = evaluate_forecasts_peer_spot_forecast(
                forecasts,
                resolution_bucket,
                spot_forecast_timestamp,
                question.type,
            )
        case score_types.RELATIVE_LEGACY:
            # TODO: fill this out
            scores = evaluate_forecasts_legacy_relative(
                forecasts,
                resolution_bucket,
                0,
                0,
                question.type,
            )
        case other:
            raise NotImplementedError(f"Score type {other} not implemented")

    scores: list[Score] = []
    users = {forecast.author for forecast in forecasts}
    for user in users:
        user_score = 0
        user_coverage = 0
        for forecast, score in zip(forecasts, forecast_scores):
            if forecast.author == user:
                user_score += score.score
                user_coverage += score.coverage
        scores.append(
            Score(
                user=user,
                score=user_score,
                coverage=user_coverage,
                score_type=score_type,
            )
        )
    return scores