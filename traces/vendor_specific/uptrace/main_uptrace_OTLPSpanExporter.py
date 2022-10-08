from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
#from common import get_tracer
import os
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
#import uptrace
import grpc
from traces.vendor_specific.uptrace.dsn_helper import parse_dsn, DSN


def get_otlp_exporter():
    dsn = "https://lHBrBFFwBfqMei7yNieoWA@uptrace.dev/861"
    dsn = parse_dsn(dsn)
    print(dsn.str)
    print(dsn.otlp_grpc_addr)
    credentials = grpc.ssl_channel_credentials()

    exporter = OTLPSpanExporter(
        endpoint=dsn.otlp_grpc_addr,
        # credentials=credentials,
        headers=(("uptrace-dsn", dsn.str),),
        timeout=5,
        compression=grpc.Compression.Gzip,
    )

    return exporter


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
