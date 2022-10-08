from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
#from common import get_tracer
import os
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

otlp_vendors = {
    "uptrace": {"endpoint": "https://otlp.uptrace.dev:4317", "headers": (("uptrace-dsn", "https://lHBrBFFwBfqMei7yNieoWA@uptrace.dev/861"),), },
    "honeycomb": {"endpoint": "https://api.honeycomb.io/", "headers": (("x-honeycomb-team", "AM4JdEbIwYwxt27Ese0fJI"),), },
    "lightstep": {"endpoint": "ingest.lightstep.com:443", "headers": (("lightstep-access-token", "AYersInhmO2hq1lwz2JAXNCY5VgAdkGLn+xTq0mplv0sBPXQUDWj3lljaVJnDR6pCqCEXg7K0l3My0ckLgC1+34CR4+1CwGaS6WPi8K+"),), },
    "aspecto": {"endpoint": "otelcol.aspecto.io:4317", "headers": (("authorization", "e0dea5ab-a9c0-49fc-a389-14a7fb938ced"),), },
}

provider = TracerProvider()
if not os.environ.get("OTEL_RESOURCE_ATTRIBUTES"):
    # Service name is required for most backends
    resource = Resource(attributes={
        SERVICE_NAME: "service_name",
    })
    #log_level = "DEBUG",
    provider = TracerProvider(resource=resource)
    print("Service name : " + "service_name")


def get_otlp_exporter(vendor):
    return OTLPSpanExporter(
        endpoint=otlp_vendors[vendor]['endpoint'],
        headers=otlp_vendors[vendor]['headers']
    )


def get_tracer(vendor):

    #vendor = "aspecto"
    #vendor = "uptrace"
    #vendor = "honeycomb"
    #vendor = "lightstep"
    span_exporter = get_otlp_exporter(vendor)
    service_name = "manual_"+vendor

    processor = BatchSpanProcessor(span_exporter)
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    return trace.get_tracer(__name__)
