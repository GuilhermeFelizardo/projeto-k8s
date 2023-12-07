import os
import random
import time
import requests
from flask import Flask
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.semconv.resource import ResourceAttributes
from prometheus_flask_exporter import PrometheusMetrics

# Inicializa a aplicação Flask
app = Flask(__name__)

# Configurações do Prometheus
def configure_prometheus(app):
    PrometheusMetrics(app)

# Configurações do OpenTelemetry
def configure_opentelemetry():
    tempo_endpoint = os.environ.get("TEMPO_ENDPOINT")
    resource = Resource(attributes={ResourceAttributes.SERVICE_NAME: "servico-principal"})
    trace.set_tracer_provider(TracerProvider(resource=resource))
    otlp_exporter = OTLPSpanExporter(endpoint=tempo_endpoint, insecure=True)
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))
    FlaskInstrumentor().instrument_app(app)
    RequestsInstrumentor().instrument()

# Definição das rotas da aplicação
def setup_routes(app):
    @app.route("/")
    def home():
        random_sleep()
        return "Bem-vindo ao Serviço Principal!"

    @app.route("/chamada")
    def internal_call():
        random_sleep()
        try:
            response = requests.get(os.environ.get("SERVICO_EXTERNO_URL"))
            return f"Resposta do serviço externo: {response.text}"
        except requests.RequestException:
            return {"error": "Erro ao chamar o serviço externo"}, 500

    @app.route("/info")
    def info():
        random_sleep()
        return "Informações do Serviço"

    @app.route("/status")
    def status():
        random_sleep()
        return "Status do Serviço: Ativo"

    @app.route("/contato")
    def contato():
        random_sleep()
        return "Contato do Serviço"

# Função auxiliar para simular atraso
def random_sleep():
    time.sleep(random.uniform(0, 5))

if __name__ == '__main__':
    configure_prometheus(app)
    configure_opentelemetry()
    setup_routes(app)
    app.run(host='0.0.0.0', port=5000)
