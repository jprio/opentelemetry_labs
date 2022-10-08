from opentelemetry.launcher import configure_opentelemetry
from opentelemetry import trace

import socket
configure_opentelemetry(
    access_token="AYersInhmO2hq1lwz2JAXNCY5VgAdkGLn+xTq0mplv0sBPXQUDWj3lljaVJnDR6pCqCEXg7K0l3My0ckLgC1+34CR4+1CwGaS6WPi8K+",
    span_exporter_endpoint="https://ingest.lightstep.com:443",

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
