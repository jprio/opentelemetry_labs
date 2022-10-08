from argparse import REMAINDER, ArgumentParser
from pkg_resources import iter_entry_points
from shutil import which
from re import sub
from os.path import abspath, dirname, pathsep
from os import environ, execl, getcwd
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


def get_otlp_exporter(vendor):
    return OTLPSpanExporter(
        endpoint=otlp_vendors[vendor]['endpoint'],
        headers=otlp_vendors[vendor]['headers']
    )


def get_tracer():

    vendor = "aspecto"
    #vendor = "uptrace"
    #vendor = "honeycomb"
    #vendor = "lightstep"
    span_exporter = get_otlp_exporter("aspecto")
    service_name = "manual_"+vendor
    provider = TracerProvider()
    if not os.environ.get("OTEL_RESOURCE_ATTRIBUTES"):
        # Service name is required for most backends
        resource = Resource(attributes={
            SERVICE_NAME: service_name,
        })
        #log_level = "DEBUG",
        provider = TracerProvider(resource=resource)
        print("Service name : " + service_name)

    processor = BatchSpanProcessor(span_exporter)
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    return trace.get_tracer(__name__)


def run() -> None:

    parser = ArgumentParser(
        description="""
        opentelemetry-instrument automatically instruments a Python
        program and its dependencies and then runs the program.
        """,
        epilog="""
        Optional arguments(except for --help) for opentelemetry-instrument
        directly correspond with OpenTelemetry environment variables. The
        corresponding optional argument is formed by removing the OTEL_ or
        OTEL_PYTHON_ prefix from the environment variable and lower casing the
        rest. For example, the optional argument - -attribute_value_length_limit
        corresponds with the environment variable
        OTEL_ATTRIBUTE_VALUE_LENGTH_LIMIT.

        These optional arguments will override the current value of the
        corresponding environment variable during the execution of the command.
        """,
    )

    argument_otel_environment_variable = {}

    for entry_point in iter_entry_points(
        "opentelemetry_environment_variables"
    ):
        environment_variable_module = entry_point.load()

        for attribute in dir(environment_variable_module):

            if attribute.startswith("OTEL_"):

                argument = sub(r"OTEL_(PYTHON_)?", "", attribute).lower()
                print(argument)
                parser.add_argument(
                    f"--{argument}",
                    required=False,
                )
                argument_otel_environment_variable[argument] = attribute

    parser.add_argument("command", help="Your Python application.")
    parser.add_argument(
        "command_args",
        help="Arguments for your application.",
        nargs=REMAINDER,
    )
    args = parser.parse_args()
    print(args)
    for argument, otel_environment_variable in (
        argument_otel_environment_variable
    ).items():
        print(argument, otel_environment_variable)
        value = getattr(args, argument)
        if value is not None:
            print("==========setting : " + otel_environment_variable)
            print(otel_environment_variable, value)

            environ[otel_environment_variable] = value

    python_path = environ.get("PYTHONPATH")

    if not python_path:
        python_path = []

    else:
        python_path = python_path.split(pathsep)

    cwd_path = getcwd()

    # This is being added to support applications that are being run from their
    # own executable, like Django.
    # FIXME investigate if there is another way to achieve this
    if cwd_path not in python_path:
        python_path.insert(0, cwd_path)

    filedir_path = dirname(abspath(__file__))

    python_path = [path for path in python_path if path != filedir_path]

    python_path.insert(0, filedir_path)

    environ["PYTHONPATH"] = pathsep.join(python_path)

    executable = "/home/jp/dev/code/python/opentelemetry_labs/.venv/bin/python"
    print("executable : " + executable)
    print(*args.command_args)


run()
#tracer = get_tracer()
tracer = trace.get_tracer_provider().get_tracer(__name__)

with tracer.start_as_current_span("client operation"):
    print(os.environ)
    try:
        carrier = {}
        TraceContextTextMapPropagator().inject(carrier)
        #header = {"traceparent": carrier["traceparent"]}
        print(f"plopplopplop")
    except Exception as e:
        print(f"Failed {e}")
        pass
