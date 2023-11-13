import os
import random
import time
from flask import Flask
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

app = Flask(__name__)

# Configuração do Tracer
service_name = "academia_app"
resource = Resource(attributes={"service.name": service_name})
tracer_provider = TracerProvider(resource=resource)
trace.set_tracer_provider(tracer_provider)

# Usar variável de ambiente para o endpoint do OTLP
tempo_endpoint = os.environ.get("TEMPO_ENDPOINT", "tempo-endpoint:4317")
otlp_exporter = OTLPSpanExporter(endpoint=tempo_endpoint, insecure=True)
tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

tracer = trace.get_tracer(__name__)

def random_sleep():
    time.sleep(random.uniform(0, 3))

@app.route('/')
def hello():
    with tracer.start_as_current_span("hello-span"):
        random_sleep()
        return 'Hello, World!'

@app.route('/professores')
def listar_professores():
    with tracer.start_as_current_span("listar-professores-span"):
        random_sleep()
        professores = ["João", "Ana", "Carlos"]
        return ', '.join(professores)

@app.route('/dias-funcionamento')
def dias_funcionamento():
    with tracer.start_as_current_span("dias-funcionamento-span"):
        random_sleep()
        dias = ["Segunda a Sexta: 6h às 22h", "Sábado: 8h às 14h"]
        return ', '.join(dias)

@app.route('/aparelhos')
def listar_aparelhos():
    with tracer.start_as_current_span("listar-aparelhos-span"):
        random_sleep()
        aparelhos = ["Esteira", "Bicicleta", "Leg Press"]
        return ', '.join(aparelhos)

if __name__ == '__main__':
    app.run(debug=False)
