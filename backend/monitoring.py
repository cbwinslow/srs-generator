from flask import Blueprint, jsonify
import time
from prometheus_client import Counter, Histogram, generate_latest

bp = Blueprint("monitoring", __name__)

# Define metrics
REQUEST_COUNT = Counter(
    "srs_request_total", "Total number of SRS generation requests", ["status"]
)

REQUEST_LATENCY = Histogram(
    "srs_request_latency_seconds", "SRS generation request latency", ["endpoint"]
)


@bp.route("/health")
def health_check():
    """Basic health check endpoint."""
    return jsonify({"status": "healthy", "timestamp": time.time()})


@bp.route("/metrics")
def metrics():
    """Prometheus metrics endpoint."""
    return generate_latest(), 200, {"Content-Type": "text/plain"}


def record_request_metric(status_code):
    """Record request metrics."""
    status = "success" if status_code < 400 else "error"
    REQUEST_COUNT.labels(status=status).inc()


def start_request_timer():
    """Start timing a request."""
    return time.time()


def stop_request_timer(start_time, endpoint):
    """Stop timing a request and record the duration."""
    duration = time.time() - start_time
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(duration)
