from opentelemetry import trace
from opentelemetry.semconv.trace import SpanAttributes
import trace_helper
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator


"""
Attributes let you attach key/value pairs to a span so it carries more information about the current operation that it’s tracking.

"""

tracer = trace_helper.get_tracer("uptrace")


@tracer.start_as_current_span("do_work_decorated")
def trace_attributes():
    current_span = trace.get_current_span()

    current_span.set_attribute("operation.value", 1)
    current_span.set_attribute("operation.name", "Saying hello!")
    current_span.set_attribute("operation.other-stuff", [1, 2, 3])
    try:
        carrier = {}
        TraceContextTextMapPropagator().inject(carrier)
        #header = {"traceparent": carrier["traceparent"]}
        print(f"plopplopplop")

    except Exception as e:
        print(f"Failed {e}")
        pass


@tracer.start_as_current_span("do_work_decorated")
def trace_semantic_attributes():
    current_span = trace.get_current_span()
    current_span.set_attribute(SpanAttributes.HTTP_METHOD, "GET")
    current_span.set_attribute(
        SpanAttributes.HTTP_URL, "https://opentelemetry.io/")
    try:
        carrier = {}
        TraceContextTextMapPropagator().inject(carrier)
        #header = {"traceparent": carrier["traceparent"]}
        print(f"plopplopplop")

    except Exception as e:
        print(f"Failed {e}")
        pass


trace_attributes()
