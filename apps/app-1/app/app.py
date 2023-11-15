import os
import logging
from flask import Flask, request
import requests
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.semconv.resource import ResourceAttributes

app = Flask(__name__)

# Configurar logging
logging.basicConfig(level=logging.INFO)

# Configuração do OpenTelemetry para Produção
tempo_endpoint = os.environ.get("TEMPO_ENDPOINT")
servico_externo_url = os.environ.get("SERVICO_EXTERNO_URL")

if not tempo_endpoint or not servico_externo_url:
    raise RuntimeError("As variáveis de ambiente TEMPO_ENDPOINT e SERVICO_EXTERNO_URL são obrigatórias.")

resource = Resource(attributes={ResourceAttributes.SERVICE_NAME: "servico-principal"})
trace.set_tracer_provider(TracerProvider(resource=resource))
otlp_exporter = OTLPSpanExporter(endpoint=tempo_endpoint, insecure=True)  # Considerar segurança de transporte
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

@app.route("/")
def home():
    return "Bem-vindo ao Serviço Principal!"

@app.route("/chamada-interna")
def internal_call():
    try:
        response = requests.get(servico_externo_url)
        return f"Resposta do serviço externo: {response.text}"
    except requests.RequestException as e:
        logging.error(f"Erro ao chamar o serviço externo: {e}")
        return {"error": "Erro ao chamar o serviço externo"}, 500

if __name__ == "__main__":
    # Não use o servidor de desenvolvimento em produção
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
