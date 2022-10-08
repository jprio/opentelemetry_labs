#!/home/jp/dev/code/python/opentelemetry_labs/.venv/bin/python3.9

from opentelemetry.launcher import configure_opentelemetry
from argparse import REMAINDER, ArgumentParser
from pkg_resources import iter_entry_points
from shutil import which
from re import sub
from os.path import abspath, dirname, pathsep
from os import environ, execl, getcwd
from logging import getLogger
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
import os
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
import unittest
import trace_helper
import time
import opentelemetry


class TestStringMethods(unittest.TestCase):

    # @unittest.skip("reason for skipping")
    def test_simple_aspecto(self):
        tracer = trace_helper.get_tracer("aspecto")

        with tracer.start_as_current_span("client operation"):
            try:
                carrier = {}
                TraceContextTextMapPropagator().inject(carrier)
                header = {"traceparent": carrier["traceparent"]}
                # res = requests.get(url, headers=header)
                print(f"Request ")
            except Exception as e:
                print(f"Request failed {e}")
                pass

    # @unittest.skip("reason for skipping")
    def test_simple_lightstep(self):
        tracer = trace_helper.get_tracer("lightstep")
        with tracer.start_as_current_span("client operation"):
            try:
                carrier = {}
                TraceContextTextMapPropagator().inject(carrier)
                header = {"traceparent": carrier["traceparent"]}
                # res = requests.get(url, headers=header)
                print(f"Request ")
                with tracer.start_as_current_span("inner_client operation"):
                    try:
                        carrier = {}
                        TraceContextTextMapPropagator().inject(carrier)
                        header = {"traceparent": carrier["traceparent"]}
                        # res = requests.get(url, headers=header)
                        print(f"Request ")
                    except Exception as e:
                        print(f"Request  {e}")
                        pass
            except Exception as e:
                print(f"Request  {e}")
                pass

        # trace.get_tracer_provider().shutdown()
        # time.sleep(3)

    @unittest.skip("reason for skipping")
    def test_autoinstrument(self):

        # exporter_otlp_traces_endpoint
        # exporter_otlp_traces_headers
        env_bak = os.environ
        # os.environ["traces_exporter"] = "otlp_proto_http,otlp_proto_grpc"
        """
        os.environ["traces_exporter"] = "console"
        os.environ["service_name"] = "test-autoinstr"
        os.environ["exporter_otlp_traces_headers"] = "lightstep-access-token=AYersInhmO2hq1lwz2JAXNCY5VgAdkGLn+xTq0mplv0sBPXQUDWj3lljaVJnDR6pCqCEXg7K0l3My0ckLgC1+34CR4+1CwGaS6WPi8K+"
        os.environ["exporter_otlp_traces_endpoint"] = "ingest.lightstep.com:443"
        os.environ["exporter_otlp_endpoint"] = "ingest.lightstep.com:443"
        os.environ["OTEL_TRACES_EXPORTER"] = "console,otlp_proto_http"
        os.environ["OTEL_SERVICE_NAME"] = "test-autoinstr"
        os.environ["otel_exporter_otlp_traces_headers".upper(
        )] = "lightstep-access-token=AYersInhmO2hq1lwz2JAXNCY5VgAdkGLn+xTq0mplv0sBPXQUDWj3lljaVJnDR6pCqCEXg7K0l3My0ckLgC1+34CR4+1CwGaS6WPi8K+"
        os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = "lightstep-access-token = AYersInhmO2hq1lwz2JAXNCY5VgAdkGLn+xTq0mplv0sBPXQUDWj3lljaVJnDR6pCqCEXg7K0l3My0ckLgC1+34CR4+1CwGaS6WPi8K +"
        os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "https://ingest.lightstep.com:443"
        os.environ["otel_exporter_otlp_endpoint".upper()
                   ] = "https://ingest.lightstep.com:443"
        os.environ["OTEL_PYTHON_TRACER_PROVIDER"] = "sdk_tracer_provider"
        os.environ["OTEL_LOG_LEVEL"] = "debug"
        print("otel_exporter_otlp_endpoint".upper())

        print(os.environ)
        print(tracer)
        """
        tracer = trace.get_tracer_provider().get_tracer(__name__)

        @tracer.start_as_current_span("do_roll")
        def fonction():
            with tracer.start_as_current_span("client operation"):
                print(f"Autoinstr ")

        with tracer.start_as_current_span("client ops"):
            print("pouet")

        os.environ = env_bak


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
    print("passre args")
    args = parser.parse_args()

    for argument, otel_environment_variable in (
        argument_otel_environment_variable
    ).items():
        print(argument, otel_environment_variable)
        value = getattr(args, argument)
        if value is not None:

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

    executable = which(args.command)
    print(executable)


if __name__ == '__main__':
    import re
    import sys
    # from opentelemetry.instrumentation.auto_instrumentation import run
    print(re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0]))
    # sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    unittest.main()
