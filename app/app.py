# app.py (Exemplo de API com OpenTelemetry)
from flask import Flask
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

app = Flask(__name__)
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)

# Configurar o exportador OTLP para enviar traces ao backend (ex. Tempo)
otlp_exporter = OTLPSpanExporter(endpoint="tempo-endpoint:4317", insecure=True)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

@app.route('/')
def hello():
    with tracer.start_as_current_span("hello-span"):
        return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
