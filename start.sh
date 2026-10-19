#!/bin/bash

OTEL_SERVICE_NAME="fastapi-url-shortener" \
OTEL_METRICS_EXPORTER="none" \
OTEL_TRACES_EXPORTER="otlp" \
OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4317" \
OTEL_EXPORTER_OTLP_INSECURE="true" \
uv run opentelemetry-instrument fastapi dev main.py
