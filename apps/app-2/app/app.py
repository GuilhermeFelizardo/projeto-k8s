import os
import logging
from flask import Flask
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.semconv.resource import ResourceAttributes

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Configuração do OpenTelemetry para Produção
tempo_endpoint = os.environ.get("TEMPO_ENDPOINT")
if not tempo_endpoint:
    raise RuntimeError("A variável de ambiente TEMPO_ENDPOINT é obrigatória.")

resource = Resource(attributes={ResourceAttributes.SERVICE_NAME: "servico-externo"})
trace.set_tracer_provider(TracerProvider(resource=resource))
otlp_exporter = OTLPSpanExporter(endpoint=tempo_endpoint, insecure=True)  # Considerar segurança de transporte
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))
FlaskInstrumentor().instrument_app(app)

@app.route("/externo")
def external():
    return "Resposta do Serviço Externo"

if __name__ == "__main__":
    # Não use o servidor de desenvolvimento em produção
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
