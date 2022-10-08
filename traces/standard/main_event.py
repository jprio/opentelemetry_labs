from opentelemetry import trace
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
import trace_helper
tracer = trace_helper.get_tracer("uptrace")

"""
An event is a human-readable message on a span that represents “something happening” during its lifetime. You can think of it as a primitive log.

"""


@tracer.start_as_current_span("do_work_decorated")
def trace_event():
    current_span = trace.get_current_span()
    current_span.add_event("Gonna try it!")

# Do the thing

    try:
        carrier = {}
        TraceContextTextMapPropagator().inject(carrier)
        print(f"plopplopplop")

    except Exception as e:
        print(f"Failed {e}")
        pass

    current_span.add_event("Did it!")


trace_event()
