#!/usr/bin/env python3

from opentelemetry.sdk._metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from typing import Iterable
from opentelemetry.exporter.otlp.proto.grpc._metric_exporter import OTLPMetricExporter
#import uptrace
from opentelemetry import _metrics
from opentelemetry._metrics import get_meter_provider, set_meter_provider
from opentelemetry.sdk._metrics import MeterProvider
from opentelemetry.sdk._metrics.export import PeriodicExportingMetricReader
import time
import threading
import random

ls_access_token = "AYersInhmO2hq1lwz2JAXNCY5VgAdkGLn+xTq0mplv0sBPXQUDWj3lljaVJnDR6pCqCEXg7K0l3My0ckLgC1+34CR4+1CwGaS6WPi8K+"

exporter = OTLPMetricExporter(
    endpoint="ingest.lightstep.com:443",
    headers=(("lightstep-access-token", ls_access_token),),
)

exporter = ConsoleMetricExporter()
reader = PeriodicExportingMetricReader(exporter)
provider = MeterProvider(metric_readers=[reader])
set_meter_provider(provider)
# Counter
meter = get_meter_provider().get_meter("getting-started", "0.1.2")


def counter():
    counter = meter.create_counter("some.prefix.counter", description="TODO")

    while True:
        counter.add(1)
        time.sleep(1)


def up_down_counter():
    counter = meter.create_up_down_counter(
        "some.prefix.up_down_counter", description="TODO"
    )

    while True:
        if random.random() >= 0.5:
            counter.add(+1)
        else:
            counter.add(-1)
        time.sleep(1)


def histogram():
    histogram = meter.create_histogram(
        "some.prefix.histogram",
        description="TODO",
        unit="microseconds",
    )

    while True:
        histogram.record(random.randint(1, 5000000),
                         attributes={"attr1": "value1"})
        time.sleep(1)


def main():
    # Configure OpenTelemetry with sensible defaults.
    """
    uptrace.configure_opentelemetry(
        # Set dsn or UPTRACE_DSN env var.
        dsn="https://lHBrBFFwBfqMei7yNieoWA@uptrace.dev/861",
        service_name="myservice",
        service_version="1.0.0",
    )
    """

    threading.Thread(target=counter).start()
    threading.Thread(target=up_down_counter).start()
    threading.Thread(target=histogram).start()

    """meter = get_meter_provider().get_meter(__name__)    """

    counter2 = meter.create_counter("first_counter")
    counter2.add(1)
    print("reporting measurements to Uptrace... (press Ctrl+C to stop)")
    time.sleep(10)


if __name__ == "__main__":
    main()
