from opentelemetry.trace import Status, StatusCode
from opentelemetry import trace
import trace_helper
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

tracer = trace_helper.get_tracer("uptrace")

"""
A status can be set on a span, typically used to specify that a span has not completed successfully - StatusCode.ERROR. 
In rare scenarios, you could override the Error status with StatusCode.OK, but don’t set StatusCode.OK on successfully-completed spans.
The status can be set at any time before the span is finished:
"""


@tracer.start_as_current_span("test status")
def trace_status():
    current_span = trace.get_current_span()

    try:
        carrier = {}
        TraceContextTextMapPropagator().inject(carrier)
        print(f"plopplopplop")

    except Exception as e:
        print(f"Failed {e}")
        pass
    current_span.set_status(Status(StatusCode.ERROR))


@tracer.start_as_current_span("test status")
def trace_record_exception():
    current_span = trace.get_current_span()

    try:
        # something that might fail
        a = 1/0
        # Consider catching a more specific exception in your code
    except Exception as ex:
        current_span.set_status(Status(StatusCode.ERROR))
        current_span.record_exception(ex)


trace_status()
trace_record_exception()
