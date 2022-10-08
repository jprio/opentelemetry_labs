from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
#from common import get_tracer
import os
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator


def get_otlp_exporter():
    return OTLPSpanExporter(
        endpoint="otelcol.aspecto.io:4317",
        headers=(
            ("authorization", "e0dea5ab-a9c0-49fc-a389-14a7fb938ced"),),

    )


def get_tracer():
    span_exporter = get_otlp_exporter()

    provider = TracerProvider()
    if not os.environ.get("OTEL_RESOURCE_ATTRIBUTES"):
        # Service name is required for most backends
        resource = Resource(attributes={
            SERVICE_NAME: "test-py-manual-otlp",
        })
        #log_level = "DEBUG",
        provider = TracerProvider(resource=resource)
        print("Using default service name")

    processor = BatchSpanProcessor(span_exporter)
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    return trace.get_tracer(__name__)


tracer = get_tracer()
url = "http://"
with tracer.start_as_current_span("client operation"):
    try:
        carrier = {}
        TraceContextTextMapPropagator().inject(carrier)
        header = {"traceparent": carrier["traceparent"]}
        #res = requests.get(url, headers=header)
        print(f"Request to {url}")
    except Exception as e:
        print(f"Request to {url} failed {e}")
        pass
