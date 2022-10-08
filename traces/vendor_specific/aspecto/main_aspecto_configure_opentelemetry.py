from opentelemetry.launcher import configure_opentelemetry
from opentelemetry import trace

import socket
configure_opentelemetry(
    access_token="e0dea5ab-a9c0-49fc-a389-14a7fb938ced",
    span_exporter_endpoint="https://otelcol.aspecto.io:4317",

    service_name="service-123",
    service_version="1.2.3",
    resource_attributes={
        "host.hostname":  "http://localhost",
        "container.name": "my-container-name",
        "cloud.region": "us-central1",
        "metrics.exporter": "none"
    },
    log_level="DEBUG"

)
tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("foo") as span:
    span.set_attribute("attr1", "valu1")
    with tracer.start_as_current_span("bar"):
        with tracer.start_as_current_span("baz"):
            print("Hello world from OpenTelemetry Python!")
print("Hello OT")
