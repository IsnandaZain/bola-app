import time

from flask import request
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    "request_count", "App Request Count",
    ["app_name", "method", "endpoint", "http_status"]
)

REQUEST_LATENCY = Histogram(
    "request_latency_seconfs", "Request latency",
    ["app_name", "method", "endpoint", "http_status"]
)


def start_timer():
    request.start_time = time.time()


def stop_timer(response):
    resp_time = time.time() - request.start_time
    REQUEST_LATENCY.labels("bola-app", request.method, request.url_rule, response.status_code).observe(resp_time)
    return response


def record_request_data(response):
    REQUEST_COUNT.labels("bola-app", request.method, request.url_rule, response.status_code).inc()
    return response


def setup_metrics(app):
    app.before_request(start_timer)
    app.after_request(record_request_data)
    app.after_request(stop_timer)